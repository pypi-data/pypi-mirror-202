use std::vec;

use pyo3::prelude::*;

#[pyclass]
#[derive(Clone)]
struct Point {
    #[pyo3(get)]
    x: f32,
    #[pyo3(get)]
    y: f32,
    #[pyo3(get)]
    data: Option<PyObject>
}

#[pyclass]
#[derive(Clone)]
struct Rect {
    center_x: f32,
    center_y: f32,
    width: f32,
    height: f32,
    west_edge: f32,
    east_edge: f32,
    north_edge: f32,
    south_edge: f32
}

#[pyclass]
struct QuadTree {
    boundary: Rect,
    max_points: usize,
    points: Vec<Point>,
    depth: u32,
    divided: bool,
    north_west: Option<Box<Self>>,
    north_east: Option<Box<Self>>,
    south_east: Option<Box<Self>>,
    south_west: Option<Box<Self>>,
}

#[pymethods]
impl Point {
    #[new]
    fn __new__(x: f32, y: f32, data: Option<PyObject>) -> Self {
        return Self {
            x, y, data
        }
    }

    fn __repr__(&self) -> String {
        if let Some(data) = &self.data {
            std::format!("Point(x={}, y={}, data={})", self.x, self.y, data)
        } else {
            std::format!("Point(x={}, y={})", self.x, self.y)
        }
    }

    fn __str__(&self) -> String {
        return self.__repr__()
    }

    fn distance_to(&self, other: &Point) -> f32 {
        let x_diff = self.x - other.x;
        let y_diff = self.y - other.y;

        f32::sqrt(x_diff*x_diff + y_diff*y_diff)
    }
}

#[pymethods]
impl Rect {
    #[new]
    fn __new__(center_x: f32, center_y: f32, width: f32, height: f32) -> Self {
        let west_edge = center_x - (width / 2.);
        let east_edge = center_x + (width / 2.);
        let north_edge = center_y - (height / 2.);
        let south_edge = center_y + (height / 2.);

        Self {
            center_x,
            center_y,
            width,
            height,
            west_edge,
            east_edge,
            north_edge,
            south_edge
        }
    }

    fn contains(&self, point: &Point) -> bool {
        point.x >= self.west_edge
        && point.x < self.east_edge
        && point.y >= self.north_edge
        && point.y < self.south_edge
    }

    fn intersects(&self, rect: &Rect) -> bool {
        !(
            rect.west_edge > self.east_edge
            || rect.east_edge < self.west_edge
            || rect.north_edge > self.south_edge
            || rect.south_edge < self.north_edge
        )
    }
}

#[pymethods]
impl QuadTree {
    #[new]
    fn __new__(boundary: Rect, max_points: usize, depth: u32) -> Self {
        Self {
            boundary,
            max_points,
            depth,
            divided: false,
            points: vec![],
            north_east: None,
            north_west: None,
            south_east: None,
            south_west: None
        }
    }

    fn __len__(&self) -> usize {
        let mut result = self.points.len();

        if self.divided {
            if let Some(north_east) = &self.north_east {
                result += north_east.__len__();
            }

            if let Some(north_west) = &self.north_west {
                result += north_west.__len__();
            }

            if let Some(south_east) = &self.south_east {
                result += south_east.__len__();
            }

            if let Some(south_west) = &self.south_west {
                result += south_west.__len__();
            }
        }

        result
    }

    fn divide(&mut self) {
        let center_x = self.boundary.center_x;
        let center_y = self.boundary.center_y;
        let width = self.boundary.width / 2.;
        let height = self.boundary.height / 2.;

        let boundary = Rect::__new__(
            center_x - width / 2.,
            center_y - height / 2.,
            width, height);
        let north_west = QuadTree::__new__(
            boundary,
            self.max_points, self.depth + 1);

        let boundary = Rect::__new__(
            center_x + width / 2.,
            center_y - height / 2.,
            width, height);
        let north_east = QuadTree::__new__(
            boundary,
            self.max_points, self.depth + 1);

        let boundary = Rect::__new__(
            center_x + width / 2.,
            center_y + height / 2.,
            width, height);
        let south_east = QuadTree::__new__(
            boundary,
            self.max_points, self.depth + 1);

        let boundary = Rect::__new__(
            center_x - width / 2.,
            center_y + height / 2.,
            width, height);
        let south_west = QuadTree::__new__(
            boundary,
            self.max_points, self.depth + 1);

        self.north_west = Some(Box::new(north_west));
        self.north_east = Some(Box::new(north_east));
        self.south_east = Some(Box::new(south_east));
        self.south_west = Some(Box::new(south_west));

        self.divided = true;
    }

    fn insert(&mut self, point: Point) -> bool {
        if !self.boundary.contains(&point) {
            return false;
        }

        if self.points.len() < self.max_points {
            self.points.insert(0, point);
            return true;
        }

        if !self.divided {
            self.divide();
        }

        self.north_east.as_mut().unwrap().insert(point.clone())
        || self.north_west.as_mut().unwrap().insert(point.clone())
        || self.south_east.as_mut().unwrap().insert(point.clone())
        || self.south_west.as_mut().unwrap().insert(point.clone())
    }

    fn query_rect(&self, boundary: &Rect) -> Vec<Point> {
        if !self.boundary.intersects(&boundary) {
            vec![]
        } else {
            let mut result: Vec<Point> =
                self.points.clone().into_iter()
                .filter(|p| boundary.contains(p))
                .collect();
            
            if self.divided {
                if let Some(north_east) = &self.north_east {
                    result.append(&mut north_east.query_rect(boundary))
                }

                if let Some(north_west) = &self.north_west {
                    result.append(&mut north_west.query_rect(boundary))
                }

                if let Some(south_east) = &self.south_east {
                    result.append(&mut south_east.query_rect(boundary))
                }

                if let Some(south_west) = &self.south_west {
                    result.append(&mut south_west.query_rect(boundary))
                }
            }

            result
        }
    }

    fn query_radius(&self, center_x: f32, center_y: f32, radius: f32) -> Vec<Point> {
        let boundary = Rect::__new__(center_x, center_y, 2.*radius, 2.*radius);
        let center_point = Point::__new__(center_x, center_y, None);

        if !self.boundary.intersects(&boundary) {
            vec![]
        } else {
            let mut result: Vec<Point> =
                self.points.clone().into_iter()
                .filter(|p| boundary.contains(p))
                .filter(|p| p.distance_to(&center_point) < radius)
                .collect();

                if let Some(north_east) = &self.north_east {
                    result.append(&mut north_east.query_radius(center_x, center_y, radius))
                }

                if let Some(north_west) = &self.north_west {
                    result.append(&mut north_west.query_radius(center_x, center_y, radius))
                }

                if let Some(south_east) = &self.south_east {
                    result.append(&mut south_east.query_radius(center_x, center_y, radius))
                }

                if let Some(south_west) = &self.south_west {
                    result.append(&mut south_west.query_radius(center_x, center_y, radius))
                }

            result
        }
    }
}

/// A Python module implemented in Rust.
#[pymodule]
fn quadtree(_py: Python, m: &PyModule) -> PyResult<()> {
    m.add_class::<Point>()?;
    m.add_class::<Rect>()?;
    m.add_class::<QuadTree>()?;
    Ok(())
}