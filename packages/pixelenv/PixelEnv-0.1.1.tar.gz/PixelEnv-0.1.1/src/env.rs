use pyo3::prelude::*;

#[pyclass]
pub struct PixelEnv {
   pos: f32,
}


#[pymethods]
impl PixelEnv {
    #[new]
    pub fn new() -> Self {
        PixelEnv { pos: 0.0 }
    }

    pub fn reset(&mut self) -> PyResult<Vec<f32>> {
        self.pos = 0.0;
        return Ok(vec![self.pos]);
    }

    pub fn step(&mut self, action: i32) -> PyResult<Vec<f32>> {
        self.pos = self.pos + action as f32;
        return Ok(vec![self.pos, 1.0]);
    }

}