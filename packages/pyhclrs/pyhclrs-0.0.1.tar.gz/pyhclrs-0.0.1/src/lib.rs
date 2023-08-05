use hcl::{self, Error, Value};
use pyo3::create_exception;
use pyo3::prelude::*;
use std::collections::HashMap;

create_exception!(pyhrs, HclError, pyo3::exceptions::PyException);

struct HCLError(Error);

impl From<Error> for HCLError {
    fn from(error: Error) -> Self {
        Self(error)
    }
}

impl From<HCLError> for PyErr {
    fn from(error: HCLError) -> Self {
        HclError::new_err(error.0.to_string())
    }
}

struct HclValue(Value);

impl IntoPy<PyObject> for HclValue {
    fn into_py(self, py: Python<'_>) -> PyObject {
        match self {
            HclValue(x) => match x {
                Value::Null => None::<&str>.into_py(py),
                Value::String(value) => value.into_py(py),
                Value::Bool(value) => value.into_py(py),
                Value::Number(value) => {
                    if value.is_u64() {
                        value.as_u64().into_py(py)
                    } else if value.is_f64() {
                        value.as_f64().into_py(py)
                    } else {
                        value.as_i64().into_py(py)
                    }
                }
                Value::Array(value) => value
                    .into_iter()
                    .map(|v| HclValue(v).into_py(py))
                    .collect::<Vec<PyObject>>()
                    .into_py(py),
                Value::Object(value) => value
                    .into_iter()
                    .map(|(k, v)| (k, HclValue(v).into_py(py)))
                    .collect::<HashMap<String, PyObject>>()
                    .into_py(py),
            },
        }
    }
}

#[pyfunction]
fn loads(source: &str) -> PyResult<HclValue> {
    match hcl::from_str(source) {
        Ok(value) => Ok(HclValue(value)),
        Err(err) => Err(HCLError::from(err).into()),
    }
}

#[pymodule]
fn pyhclrs(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(loads, m)?)?;
    m.add("HCLError", _py.get_type::<HclError>())?;
    Ok(())
}
