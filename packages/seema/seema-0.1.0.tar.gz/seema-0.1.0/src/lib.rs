use std::path::Path;

use pyo3::prelude::*;
use wordcut_engine::replacer::ImmRule;
use wordcut_engine::Wordcut;
use wordcut_engine::{
    default_dict_path, load_cluster_rules, thai_cluster_path, thai_replace_rules_path,
};
use wordcut_engine::{load_dict, replacer};

#[pyclass(subclass)]
struct Seema {
    wordcut: Wordcut,
    replace_rules: Vec<ImmRule>,
}

#[pymethods]
impl Seema {
    #[new]
    fn new() -> Self {
        let dict = load_dict(default_dict_path()).unwrap();
        let replace_rules = replacer::load_imm_rules(thai_replace_rules_path().unwrap())
            .expect("Load replace rules");
        let cluster_re = load_cluster_rules(Path::new(&thai_cluster_path().unwrap())).unwrap();
        let wordcut = Wordcut::new_with_cluster_re(dict, cluster_re);
        Seema {
            wordcut,
            replace_rules,
        }
    }

    /// word tokenize
    fn segment_into_strings(&self, text: &str) -> PyResult<Vec<String>> {
        let mod_text = replacer::replace(&self.replace_rules, text);
        Ok(self.wordcut.segment_into_strings(&mod_text))
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn seema(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Seema>()?;
    Ok(())
}
