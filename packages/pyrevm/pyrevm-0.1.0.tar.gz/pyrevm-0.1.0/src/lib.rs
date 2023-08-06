// Annoying false positive lint:
// address: &str,
//   |       ^ help: if you would like to reborrow, try removing `&*`: `&`
//   |
//   = note: `#[warn(clippy::borrow_deref_ref)]` on by default
//
#![allow(clippy::borrow_deref_ref)]
#![allow(clippy::too_many_arguments)]

use pyo3::prelude::*;

mod types;
pub use types::*;

mod evm;
pub use evm::EVM;

mod utils;

#[pymodule]
fn pyrevm(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<EVM>()?;

    // Types
    m.add_class::<AccountInfo>()?;
    m.add_class::<EvmOpts>()?;

    m.add_class::<Env>()?;
    m.add_class::<CfgEnv>()?;
    m.add_class::<TxEnv>()?;
    m.add_class::<BlockEnv>()?;

    Ok(())
}
