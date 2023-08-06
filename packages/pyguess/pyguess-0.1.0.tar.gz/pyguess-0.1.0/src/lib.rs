//! This crate is aimed to be a simple and fast solution for text-matching from the file with
//! more than 2 millions of lines, especially for streets in Switzerland.
//!
//! Also, it serves as my first Rust project used for work and published out to the people
use guess_rs::{self, Candidate, Config, Sens, StreetConfig};
use guess_rs::{Place, Plz, Street};
use pyo3::prelude::*;
use std::io;

#[derive(FromPyObject)]
enum PyLocation<'a> {
    #[pyo3(transparent)]
    Place(&'a str),
    #[pyo3(transparent)]
    Plz(usize),
}

type FoundData<T> = (Option<Candidate>, Option<T>);

#[pyclass]
struct PyCandidate {
    #[pyo3(get)]
    street: Option<String>,
    #[pyo3(get)]
    location: Option<String>,
}

impl PyCandidate {
    fn from<T>(found_data: io::Result<FoundData<T>>) -> Option<Self>
    where
        T: ToString,
    {
        let found_data = found_data.ok()?;
        Some(PyCandidate {
            street: found_data.0.map(|cand| cand.text),
            location: found_data.1.map(|loc| loc.to_string()),
        })
    }
}

#[pyfunction]
fn find_street(sens: f64, street: &str, loc: Option<PyLocation>) -> Option<PyCandidate> {
    let cfg = Config {
        sens: Sens::new(sens),
        ..Config::default()
    };
    let street = Street::new(street, Some(cfg.clone())).ok()?;
    loc.map_or_else(
        || {
            PyCandidate::from(guess_rs::find_matches(
                &street,
                StreetConfig::<Plz> {
                    location: None,
                    cfg: cfg.clone(),
                },
            ))
        },
        |loc| match loc {
            PyLocation::Plz(plz) => PyCandidate::from(guess_rs::find_matches(
                &street,
                StreetConfig {
                    location: Some(Plz::new(plz)),
                    cfg: cfg.clone(),
                },
            )),
            PyLocation::Place(place) => PyCandidate::from(guess_rs::find_matches(
                &street,
                StreetConfig {
                    location: Some(Place::new(place)),
                    cfg: cfg.clone(),
                },
            )),
        },
    )
}

#[pymodule]
fn pyguess(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add("__version__", env!("CARGO_PKG_VERSION"))?;
    m.add_function(wrap_pyfunction!(find_street, m)?)?;
    m.add_class::<PyCandidate>()?;
    Ok(())
}
