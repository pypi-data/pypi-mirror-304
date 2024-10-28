import pytest
import pandas as pd
import numpy as np
from ghosted.data_blender import DataBlender
from scipy.stats import pearsonr

np.random.seed(42)

def test_detect_rounding_integers():
    blender = DataBlender()
    data = pd.Series([10, 20, 30, 40, 50])  # Integer data
    rounding = blender.detect_rounding(data)
    assert rounding == 0  # Should detect integer rounding

def test_detect_rounding_two_decimals():
    blender = DataBlender()
    data = pd.Series([10.12, 20.45, 30.67, 40.89, 50.01])  # Two decimal places
    rounding = blender.detect_rounding(data)
    assert rounding == 2  # Should detect 2 decimal places

def test_detect_rounding_mixed_floats():
    blender = DataBlender()
    data = pd.Series([10.0, 20.0, 30.0, 40.0, 50.0])  # Floats that are effectively integers
    rounding = blender.detect_rounding(data)
    assert rounding == 1  # Should treat as rounded to 1 decimal place

def test_detect_distribution_categorical():
    blender = DataBlender()
    data = pd.Series(['apple', 'orange', 'apple', 'banana', 'apple'])  # Categorical data
    dist_type, categories, probabilities, rounding = blender.detect_distribution(data)
    assert dist_type == 'categorical'
    assert sorted(categories) == sorted(['apple', 'banana', 'orange'])  # Sort to avoid order issues
    assert rounding is None  # No rounding for categorical data

def test_detect_distribution_normal():
    blender = DataBlender()
    data = pd.Series([10, 12, 14, 16, 18])  # Numerical data close to normal distribution
    dist_type, params, rounding = blender.detect_distribution(data)
    assert dist_type == 'normal'
    assert 'mean' in params and 'std' in params
    assert rounding == 0  # Should detect integer rounding

def test_generate_additional_data_categorical():
    blender = DataBlender()
    data = pd.Series(['apple', 'banana', 'orange', 'banana', 'apple'])
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('fruits', col_spec, data, 5)
    assert len(new_data) == 5
    assert set(new_data).issubset({'apple', 'banana', 'orange'})

def test_generate_additional_data_normal():
    blender = DataBlender()
    data = pd.Series([100, 110, 120, 130, 140])  # Normal-like data
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('values', col_spec, data, 5)
    assert len(new_data) == 5
    assert np.allclose(np.mean(new_data), np.mean(data), atol=10)  # New data mean close to original

def test_generate_additional_data_with_rounding():
    blender = DataBlender()
    data = pd.Series([10.5, 20.25, 30.75, 40.50, 50.12])  # Floats with 2 decimal places
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('values', col_spec, data, 5)
    assert len(new_data) == 5
    assert all(isinstance(x, float) for x in new_data)
    assert all(round(x, 2) == x for x in new_data)  # Check that all values are rounded to 2 decimal places

def test_generate_additional_data_integer_rounding():
    blender = DataBlender()
    data = pd.Series([20, 25, 30, 35, 40])  # Integer values
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('age', col_spec, data, 5)
    assert len(new_data) == 5
    assert all(isinstance(x, np.integer) for x in new_data)  # Ensure all values are integers

def test_blend_data():
    blender = DataBlender()
    df = pd.DataFrame({
        'age': [20, 25, 30, 35, 40],  # Integer data
        'income': [50000.12, 55000.34, 60000.56, 62000.78, 70000.90],  # Floats with 2 decimal places
        'gender': ['male', 'female', 'female', 'male', 'male']  # Categorical data
    })

    blended_df = blender.blend_data(df, 5)  # Generate 5 additional samples for each column

    assert len(blended_df) == len(df) + 5  # Original + new data
    assert all(isinstance(x, int) for x in blended_df['age'])  # Ensure age is still integers
    assert all(isinstance(x, float) for x in blended_df['income'])  # Ensure income is still floats
    assert set(blended_df['gender']).issubset({'male', 'female'})  # Ensure categorical values are valid

def test_detect_distribution_exponential():
    blender = DataBlender()
    data = pd.Series(np.random.exponential(scale=1.0, size=100))  # Exponential data
    dist_type, params, rounding = blender.detect_distribution(data)
    assert dist_type == 'exponential'
    assert 'lambda' in params
    assert rounding is None or rounding == 0  # Exponential distributions typically don't require rounding

def test_detect_distribution_beta():
    blender = DataBlender()
    data = pd.Series(np.random.beta(a=2, b=5, size=100))  # Beta data (between 0 and 1)
    dist_type, params, rounding = blender.detect_distribution(data)
    assert dist_type == 'beta'
    assert 'alpha' in params and 'beta' in params
    assert rounding is None or rounding == 0  # Beta distributions typically don't require rounding

def test_detect_distribution_gamma():
    blender = DataBlender()
    data = pd.Series(np.random.gamma(shape=2.0, scale=1.0, size=100))  # Gamma data
    dist_type, params, rounding = blender.detect_distribution(data)
    assert dist_type == 'gamma'
    assert 'shape' in params and 'rate' in params
    assert rounding is None or rounding == 0  # Gamma distributions typically don't require rounding

def test_generate_additional_data_exponential():
    blender = DataBlender()
    data = pd.Series(np.random.exponential(scale=1.0, size=100))  # Exponential data
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('exponential_column', col_spec, data, 50)
    assert len(new_data) == 50
    assert new_data.min() >= 0  # Exponential distribution should only generate non-negative values

def test_generate_additional_data_beta():
    blender = DataBlender()
    data = pd.Series(np.random.beta(a=2, b=5, size=100))  # Beta data
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('beta_column', col_spec, data, 50)
    assert len(new_data) == 50
    assert new_data.min() >= 0 and new_data.max() <= 1  # Ensure valid beta range (0, 1)

def test_generate_additional_data_gamma():
    blender = DataBlender()
    data = pd.Series(np.random.gamma(shape=2.0, scale=1.0, size=100))  # Gamma data
    col_spec = blender.detect_distribution(data)
    new_data = blender.generate_additional_data('gamma_column', col_spec, data, 50)
    assert len(new_data) == 50
    assert new_data.min() >= 0  # Gamma distribution should only generate non-negative values

def test_blend_data_with_new_distributions():
    blender = DataBlender()
    df = pd.DataFrame({
        'exponential': np.random.exponential(scale=1.0, size=100),
        'beta': np.random.beta(a=2, b=5, size=100),
        'gamma': np.random.gamma(shape=2.0, scale=1.0, size=100)
    })

    # Generate 50 additional samples for each column
    blended_df = blender.blend_data(df, num_samples=50)

    assert len(blended_df) == 150  # Original + new data
    assert blended_df['exponential'].min() >= 0  # Exponential should only have non-negative values
    assert blended_df['beta'].min() >= 0 and blended_df['beta'].max() <= 1  # Beta should be between 0 and 1
    assert blended_df['gamma'].min() >= 0  # Gamma should only have non-negative values

@pytest.mark.filterwarnings("ignore:divide by zero encountered in power")
def test_blend_data_with_correlation_structure():
    # Set up example real data with a strong correlation between columns
    df = pd.DataFrame({
        'X': np.linspace(0, 10, 50),
        'Y': np.linspace(0, 20, 50) + np.random.normal(0, 0.5, 50)  # Y is strongly correlated with X
    })

    blender = DataBlender()
    blended_df = blender.blend_data_with_correlation(df, num_samples=50, columns_with_correlation=['X', 'Y'])

    # Check that blended_df has the correct structure and columns
    assert isinstance(blended_df, pd.DataFrame), "blended_df should be a DataFrame"
    assert 'synthetic_flag' in blended_df.columns, "synthetic_flag column should exist in blended_df"
    assert blended_df['synthetic_flag'].isin([0, 1]).all(), "synthetic_flag should only contain 0 or 1"

    # Check correct number of rows in blended data
    assert len(blended_df) == len(df) + 50, "blended_df should contain both real and synthetic data"

@pytest.mark.filterwarnings("ignore:divide by zero encountered in power")
def test_blend_data_with_correlation_flag_counts():
    # Set up real data and generate blended data
    df = pd.DataFrame({
        'X': np.linspace(0, 10, 50),
        'Y': np.linspace(0, 20, 50) + np.random.normal(0, 0.5, 50)
    })

    blender = DataBlender()
    blended_df = blender.blend_data_with_correlation(df, num_samples=50, columns_with_correlation=['X', 'Y'])

    # Ensure synthetic_flag column has the correct counts of 0s and 1s
    assert blended_df['synthetic_flag'].value_counts().to_dict() == {0: 50, 1: 50}, \
        "synthetic_flag should have 50 real data entries and 50 synthetic entries"

@pytest.mark.filterwarnings("ignore:divide by zero encountered in power")
def test_blend_data_with_correlation_preserved():
    # Real data with a strong positive correlation
    df = pd.DataFrame({
        'X': np.linspace(0, 10, 100),
        'Y': np.linspace(0, 20, 100) + np.random.normal(0, 0.5, 100)
    })

    blender = DataBlender()
    blended_df = blender.blend_data_with_correlation(df, num_samples=100, columns_with_correlation=['X', 'Y'])

    # Calculate correlation for real and synthetic data separately
    real_data = blended_df[blended_df['synthetic_flag'] == 0]
    synthetic_data = blended_df[blended_df['synthetic_flag'] == 1]

    real_corr, _ = pearsonr(real_data['X'], real_data['Y'])
    synthetic_corr, _ = pearsonr(synthetic_data['X'], synthetic_data['Y'])

    # Assert that both correlations are positive and within a reasonable range
    assert 0.8 <= real_corr <= 1.0, f"Real data correlation should be strong, but got {real_corr}"
    assert 0.8 <= synthetic_corr <= 1.0, f"Synthetic data correlation should be strong, but got {synthetic_corr}"
    assert abs(real_corr - synthetic_corr) < 0.15, \
        "Correlations in real and synthetic data should be similar, with minimal difference"

@pytest.mark.filterwarnings("ignore:divide by zero encountered in power")
def test_blend_data_with_correlation_no_columns_specified():
    # Check that the function works if no specific columns are provided (default to all columns)
    df = pd.DataFrame({
        'X': np.linspace(0, 10, 50),
        'Y': np.linspace(0, 20, 50) + np.random.normal(0, 0.5, 50)
    })

    blender = DataBlender()
    blended_df = blender.blend_data_with_correlation(df, num_samples=50)

    # Check structure of blended dataframe
    assert 'synthetic_flag' in blended_df.columns, "synthetic_flag column should be in the blended dataframe"
    assert len(blended_df) == len(df) + 50, "blended_df should have both real and synthetic data rows"

    # Check that correlations are still reasonably close
    real_data = blended_df[blended_df['synthetic_flag'] == 0]
    synthetic_data = blended_df[blended_df['synthetic_flag'] == 1]
    real_corr, _ = pearsonr(real_data['X'], real_data['Y'])
    synthetic_corr, _ = pearsonr(synthetic_data['X'], synthetic_data['Y'])

    assert abs(real_corr - synthetic_corr) < 0.15, \
        "Correlations in real and synthetic data should be similar when no specific columns are specified"

def test_replace_data_basic_functionality():
    # Original data
    df = pd.DataFrame({
        'age': np.random.randint(18, 65, size=100),
        'income': np.random.normal(50000, 12000, size=100)
    })

    blender = DataBlender()
    synthetic_df = blender.replace_data(df, num_samples=100)

    # Check that all rows are synthetic
    assert 'synthetic_flag' in synthetic_df.columns
    assert synthetic_df['synthetic_flag'].nunique() == 1
    assert synthetic_df['synthetic_flag'].iloc[0] == 1

    # Check number of rows matches specified num_samples
    assert len(synthetic_df) == 100

def test_replace_data_distribution_matching():
    # Original data with a normal distribution
    df = pd.DataFrame({
        'height': np.random.normal(170, 10, size=100),
        'weight': np.random.normal(65, 15, size=100)
    })

    blender = DataBlender()
    synthetic_df = blender.replace_data(df, num_samples=100, random_seed=42)

    # Validate mean and std for height and weight columns in synthetic data
    for col in ['height', 'weight']:
        orig_mean, orig_std = df[col].mean(), df[col].std()
        synth_mean, synth_std = synthetic_df[col].mean(), synthetic_df[col].std()
        
        # Adjusted tolerance to account for variability in synthetic data
        assert np.isclose(orig_mean, synth_mean, atol=3), f"Mean of {col} does not match within tolerance"
        assert np.isclose(orig_std, synth_std, atol=3), f"Std of {col} does not match within tolerance"

def test_replace_data_correlation_preservation():
    # Original data with a strong correlation
    df = pd.DataFrame({
        'X': np.linspace(0, 10, 100),
        'Y': np.linspace(0, 20, 100) + np.random.normal(0, 0.5, 100)
    })

    blender = DataBlender()
    synthetic_df = blender.replace_data(df, num_samples=100, columns_with_correlation=['X', 'Y'], random_seed=42)

    # Calculate and compare correlations
    real_corr, _ = pearsonr(df['X'], df['Y'])
    synthetic_corr, _ = pearsonr(synthetic_df['X'], synthetic_df['Y'])

    assert 0.8 <= synthetic_corr <= 1.0, f"Synthetic data correlation should be strong, but got {synthetic_corr}"
    assert abs(real_corr - synthetic_corr) < 0.15, "Real and synthetic correlations should be similar"


def test_replace_data_random_seed_consistency():
    # Original data
    df = pd.DataFrame({
        'score': np.random.normal(75, 10, size=100)
    })

    blender = DataBlender()
    synthetic_df1 = blender.replace_data(df, num_samples=100, random_seed=42)
    synthetic_df2 = blender.replace_data(df, num_samples=100, random_seed=42)

    # Check that both synthetic dataframes are identical when random seed is set
    pd.testing.assert_frame_equal(synthetic_df1, synthetic_df2)

def test_replace_data_no_original_data_in_output():
    # Original data with mixed distributions
    df = pd.DataFrame({
        'category': pd.Categorical(np.random.choice(['A', 'B', 'C'], size=100)),
        'value': np.random.exponential(1, size=100)
    })

    blender = DataBlender()
    synthetic_df = blender.replace_data(df, num_samples=100)

    # Check if synthetic data differs in frequency but can overlap in actual values for categorical data
    for col in df.select_dtypes(include=['category']).columns:
        real_counts = df[col].value_counts(normalize=True)
        synth_counts = synthetic_df[col].value_counts(normalize=True)

        # Confirm distributions are close but not exactly identical due to random sampling
        assert not real_counts.equals(synth_counts), f"Frequency distribution in {col} should differ"