# Ghosted: Synthetic Data Generation and Augmentation Library

Ghosted is a Python library for generating synthetic data, augmenting existing datasets, and visualizing complex data distributions. It’s designed for data scientists, researchers, and developers who need to generate realistic synthetic data or blend synthetic data with real data for privacy-preserving applications, prototyping, testing, and educational purposes.

## Features

Ghosted offers powerful features to facilitate synthetic data generation, blending, and augmentation. Here’s a breakdown of its primary capabilities:

1. **Data Generator**: Generate synthetic data with various statistical distributions.
2. **Data Blender**: Seamlessly blend synthetic data with real data to mimic the original distribution.
3. **Anomaly Injection**: Add realistic anomalies to datasets for robust testing.
4. **Noise Injection**: Inject noise into data for simulations and noise-tolerance testing.
5. **Data Templates**: Utilize pre-built templates for synthetic data generation in popular domains like e-commerce, finance, and healthcare.
6. **Data Visualization**: Visualize distributions and relationships in synthetic and real data with histograms, KDE plots, and pairwise plots.
7. **Data Summary**: Easily generate summary statistics for both synthetic and real data.

## Installation

Ghosted is compatible with Python 3.12+. Install the library using pip:

```bash
pip install ghosted
```

## Usage

### 1. Data Generation

Ghosted's `DataGenerator` allows you to generate synthetic data from a variety of common statistical distributions. Supported distributions include, but are not limited to:

| Distribution   | Parameters                  |
|----------------|-----------------------------|
| Uniform        | `min`, `max`                |
| Normal         | `mean`, `std`               |
| Binomial       | `n`, `p`                    |
| Poisson        | `lambda`                    |
| Geometric      | `p`                         |
| Exponential    | `lambda`                    |
| Categorical    | `categories`, `probabilities` |
| Lognormal      | `mean`, `std`               |
| Beta           | `alpha`, `beta`             |
| Gamma          | `shape`, `rate`             |
| Multinomial    | `n`, `probabilities`        |
| Pareto         | `shape`                     |
| Weibull        | `shape`, `scale`            |
| Triangular     | `low`, `mode`, `high`       |
| Bernoulli      | `p`                         |

#### Example

```python
from ghosted.data_generator import DataGenerator

# Define the column specifications
column_spec = {
    'age': {'distribution': 'normal', 'mean': 35, 'std': 5},
    'income': {'distribution': 'lognormal', 'mean': 10, 'std': 2},
    'purchased': {'distribution': 'bernoulli', 'p': 0.3}
}

# Generate data
generator = DataGenerator()
synthetic_df = generator.generate_synthetic_data(column_spec, num_samples=1000)
print(synthetic_df.head())
```

### 2. Data Blending

The `DataBlender` class combines real and synthetic data, preserving the original distribution of the real dataset. This is especially useful for privacy-preserving applications.

#### Example

```python
from ghosted.data_blender import DataBlender
import pandas as pd

# Real dataset
df = pd.DataFrame({'age': [25, 45, 30], 'income': [50000, 80000, 55000]})

# Blend data
blender = DataBlender()
blended_df = blender.blend_data(df, num_samples=100)
print(blended_df.head())
```

#### Correlation Preservation
Ghosted preserves correlations between selected features, enabling better emulation of real-world data relationships.

```python
# Example with correlation preservation
blended_df_with_corr = blender.blend_data(df, num_samples=100, columns_with_correlation=['age', 'income'])
```

### 3. Anomaly Injection

The `AnomalyInjector` class allows you to add anomalies into any dataframe, supporting both extreme values and pattern-breaking injections for numeric and categorical data.

```python
from ghosted.anomaly_injector import AnomalyInjector

injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
df_with_anomalies = injector.inject_anomalies(df, columns=['income'], anomaly_type="extreme_value", factor=3)
print(df_with_anomalies.head())
```

### 4. Noise Injection

The `NoiseInjector` class lets you add controlled noise to numeric or categorical data, ideal for testing model robustness to noise.

```python
from ghosted.noise_injector import NoiseInjector

noise_injector = NoiseInjector(noise_percentage=0.1, noise_intensity=0.2, random_seed=42)
noisy_df = noise_injector.inject_noise(df, columns=['income'], noise_type="gaussian")
print(noisy_df.head())
```

### 5. Data Templates

Generate domain-specific synthetic datasets with pre-configured templates using `GenerateDataFromTemplate`.

```python
from ghosted.generate_data_from_template import GenerateDataFromTemplate

# Instantiate the template generator
template_gen = GenerateDataFromTemplate()

# View available templates
template_gen.list_templates()

# Generate a dataset for e-commerce recommendations
e_commerce_df = template_gen.generate_data('e_commerce_recommendation', num_customers=100, num_products=50)
print(e_commerce_df.head())
```

### 6. Data Visualization

Ghosted provides built-in visualization features within the `SynthDataFrame` class, enabling you to explore distributions and relationships in synthetic and blended data.

#### Key Visualization Options

- **KDE Plot**: `.visualize(kind="kde")` visualizes distribution densities.
- **Histogram**: `.visualize(kind="hist")` shows data distributions in histogram form.
- **Categorical Counts**: Visualize bar charts for categorical columns within `.visualize()`.
- **Pairwise Plot**: Analyze correlations with `.pairwise_plot(columns=[...])`.

```python
# Visualize distributions for all numerical columns
blended_df.visualize(kind="kde")

# Pairwise plot for specific columns
blended_df.pairwise_plot(columns=["age", "income", "purchased"])
```

### 7. Data Summary

Generate summary statistics for datasets, including synthetic and real data comparisons.

```python
# Get summary statistics for blended data
blended_df.summarize()
```

## Contributing

We welcome contributions! If you would like to improve or expand Ghosted, please submit a pull request or open an issue.

## License

Ghosted is licensed under the MIT License.
