use pyo3::prelude::*;
use pyo3::wrap_pyfunction;

// use lakestream;


#[pyfunction]
fn api(arg1: i32) -> PyResult<()> {
    // Call your Rust function here
    // your_function();
    println!("Hello from PyRust! {}", arg1);
    // lakestream::pytest();
    Ok(())

}

#[pymodule]
fn lakestream(py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(api, m)?)?;
    Ok(())
}

