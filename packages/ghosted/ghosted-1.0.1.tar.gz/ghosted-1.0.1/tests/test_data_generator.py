import pytest
import numpy as np
from ghosted.data_generator import DataGenerator

np.random.seed(42)


# Test cases for successful generation of data
def test_uniform_generation():
    generator = DataGenerator()
    col_spec = {'distribution': 'uniform', 'min': 0, 'max': 10}
    data = generator.generate_column(col_spec, num_samples=100)
    assert len(data) == 100
    assert (data >= 0).all() and (data <= 10).all()

def test_normal_generation():
    generator = DataGenerator()
    col_spec = {'distribution': 'normal', 'mean': 0, 'std': 1}
    data = generator.generate_column(col_spec, num_samples=100)
    assert len(data) == 100
    assert np.isclose(np.mean(data), 0, atol=0.2)
    assert np.isclose(np.std(data), 1, atol=0.2)

def test_categorical_generation():
    generator = DataGenerator()
    col_spec = {
        'distribution': 'categorical',
        'categories': ['A', 'B', 'C'],
        'probabilities': [0.2, 0.3, 0.5]
    }
    data = generator.generate_column(col_spec, num_samples=100)
    assert len(data) == 100
    assert set(data).issubset({'A', 'B', 'C'})

def test_poisson_generation():
    generator = DataGenerator()
    col_spec = {'distribution': 'poisson', 'lambda': 3}
    data = generator.generate_column(col_spec, num_samples=100)
    assert len(data) == 100
    assert (data >= 0).all()

def test_bernoulli_generation():
    generator = DataGenerator()
    col_spec = {'distribution': 'bernoulli', 'p': 0.6}
    data = generator.generate_column(col_spec, num_samples=100)
    assert len(data) == 100
    assert set(data).issubset({0, 1})

def test_weibull_generation():
    generator = DataGenerator()
    col_spec = {'distribution': 'weibull', 'shape': 1.5, 'scale': 2.0}
    data = generator.generate_column(col_spec, num_samples=100)
    assert len(data) == 100
    assert (data >= 0).all()

# Test cases for handling missing arguments
def test_uniform_missing_arguments():
    generator = DataGenerator()
    col_spec = {'distribution': 'uniform', 'min': 0}  # Missing 'max'
    with pytest.raises(ValueError) as excinfo:
        generator.generate_column(col_spec, num_samples=100)
    assert "Missing arguments for uniform distribution" in str(excinfo.value)

def test_normal_missing_arguments():
    generator = DataGenerator()
    col_spec = {'distribution': 'normal', 'mean': 0}  # Missing 'std'
    with pytest.raises(ValueError) as excinfo:
        generator.generate_column(col_spec, num_samples=100)
    assert "Missing arguments for normal distribution" in str(excinfo.value)

def test_categorical_missing_arguments():
    generator = DataGenerator()
    col_spec = {
        'distribution': 'categorical',
        'categories': ['A', 'B', 'C']  # Missing 'probabilities'
    }
    with pytest.raises(ValueError) as excinfo:
        generator.generate_column(col_spec, num_samples=100)
    assert "Missing arguments for categorical distribution" in str(excinfo.value)

def test_poisson_missing_argument():
    generator = DataGenerator()
    col_spec = {'distribution': 'poisson'}  # Missing 'lambda'
    with pytest.raises(ValueError) as excinfo:
        generator.generate_column(col_spec, num_samples=100)
    assert "Missing argument for poisson distribution" in str(excinfo.value)

def test_bernoulli_missing_argument():
    generator = DataGenerator()
    col_spec = {'distribution': 'bernoulli'}  # Missing 'p'
    with pytest.raises(ValueError) as excinfo:
        generator.generate_column(col_spec, num_samples=100)
    assert "Missing arguments for bernoulli distribution" in str(excinfo.value)
