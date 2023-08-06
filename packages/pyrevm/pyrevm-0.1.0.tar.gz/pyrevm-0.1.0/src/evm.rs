use std::fmt::Debug;

use crate::{
    types::{AccountInfo, Env},
    utils::addr,
};
use foundry_evm::executor::{fork::CreateFork, Executor};
use pyo3::exceptions::PyRuntimeError;
use pyo3::prelude::*;
use revm::db::DatabaseRef;
use ruint::aliases::U256;

use foundry_evm::executor::{opts::EvmOpts, Backend, ExecutorBuilder};

#[pyclass]
pub struct EVM(Executor);

impl EVM {
    pub fn db(&self) -> &Backend {
        self.0.backend()
    }
}

fn pyerr<T: Debug>(err: T) -> pyo3::PyErr {
    PyRuntimeError::new_err(format!("{:?}", err))
}

#[pymethods]
impl EVM {
    #[new]
    #[args(gas_limit = 18446744073709551615, tracing = false)]
    fn new(
        env: Option<Env>,
        fork_url: Option<String>,
        fork_block_number: Option<u64>,
        gas_limit: u64,
        tracing: bool,
    ) -> PyResult<Self> {
        let evm_opts = EvmOpts {
            fork_url: fork_url.clone(),
            fork_block_number,
            ..Default::default()
        };

        let fork_opts = if let Some(fork_url) = fork_url {
            let env = evm_opts.evm_env_blocking().map_err(pyerr)?;
            Some(CreateFork {
                url: fork_url,
                enable_caching: true,
                env,
                evm_opts,
            })
        } else {
            None
        };

        let db = Backend::spawn(fork_opts);

        let mut builder = ExecutorBuilder::default()
            .with_gas_limit(gas_limit.into())
            .set_tracing(tracing);

        if let Some(env) = env {
            builder = builder.with_config(env.into());
        }

        let executor = builder.build(db);

        Ok(EVM(executor))
    }

    /// Inserts the provided account information in the database at
    /// the specified address.
    fn basic(_self: PyRef<'_, Self>, address: &str) -> PyResult<Option<AccountInfo>> {
        let db = _self.0.backend();
        let acc = db.basic(addr(address)?).map_err(pyerr)?;
        Ok(acc.map(Into::into))
    }

    /// Inserts the provided account information in the database at
    /// the specified address.
    fn insert_account_info(
        mut _self: PyRefMut<'_, Self>,
        address: &str,
        info: AccountInfo,
    ) -> PyResult<()> {
        let db = _self.0.backend_mut();
        db.insert_account_info(addr(address)?, info.into());

        Ok(())
    }

    /// Set the balance of a given address.
    fn set_balance(mut _self: PyRefMut<'_, Self>, address: &str, balance: U256) -> PyResult<()> {
        _self.0.set_balance(addr(address)?, balance.into()).map_err(pyerr)?;
        Ok(())
    }

    /// Retrieve the balance of a given address.
    fn get_balance(_self: PyRef<'_, Self>, address: &str) -> PyResult<U256> {
        let balance = _self.0.get_balance(addr(address)?).map_err(pyerr)?;
        Ok(balance.into())
    }

    fn call_raw_committing(
        mut _self: PyRefMut<'_, Self>,
        caller: &str,
        to: &str,
        value: Option<U256>,
        data: Option<Vec<u8>>,
    ) -> PyResult<String> {
        let res = _self
            .0
            .call_raw_committing(
                // TODO: The constant type conversions when
                // crossing the boundary is annoying. Can we pass it
                // a type that's already an `Address`?
                addr(caller)?,
                addr(to)?,
                data.unwrap_or_default().into(),
                value.unwrap_or_default().into(),
            )
            .map_err(pyerr)?;

        if res.reverted {
            return Err(pyerr(res.exit_reason));
        }

        // TODO: Return the traces back to the user.
        dbg!(&res.traces);
        Ok(format!("{:x}", res.result))
    }

    fn call_raw(
        _self: PyRef<'_, Self>,
        caller: &str,
        to: &str,
        value: Option<U256>,
        data: Option<Vec<u8>>,
    ) -> PyResult<String> {
        let res = _self
            .0
            .call_raw(
                addr(caller)?,
                addr(to)?,
                data.unwrap_or_default().into(),
                value.unwrap_or_default().into(),
            )
            .map_err(pyerr)?;

        if res.reverted {
            return Err(pyerr(res.exit_reason));
        }

        dbg!(&res.traces);
        Ok(format!("{:x}", res.result))
    }

    /// Deploy a contract with the given code.
    fn deploy(
        mut _self: PyRefMut<'_, Self>,
        deployer: &str,
        code: Option<Vec<u8>>,
        value: Option<U256>,
        _abi: Option<&str>,
    ) -> PyResult<String> {
        let res = _self
            .0
            .deploy(
                addr(deployer)?,
                code.unwrap_or_default().into(),
                value.unwrap_or_default().into(),
                None,
            )
            .map_err(pyerr)?;

        dbg!(&res.traces);
        Ok(format!("{:?}", res.address))
    }
}