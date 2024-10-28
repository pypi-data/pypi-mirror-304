import pytest
import numpy as np
import pandas as pd
from ghosted.noise_injector import NoiseInjector

def test_gaussian_noise_injection():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = NoiseInjector(noise_percentage=0.1, noise_intensity=0.2, random_seed=42)
    noisy_df = injector.inject_noise(df, columns=['feature'], noise_type="gaussian")

    # Check that roughly 10% of rows have been altered
    num_noisy_points = int(len(df) * 0.1)
    num_changed = (noisy_df['feature'] != df['feature']).sum()
    assert num_noisy_points * 0.8 <= num_changed <= num_noisy_points * 1.2, "Incorrect number of Gaussian noise points injected"

    # Verify that noise injection is based on Gaussian distribution
    noise_diff = noisy_df['feature'] - df['feature']
    assert np.isclose(noise_diff.mean(), 0, atol=1e-1), "Mean of Gaussian noise should be near zero"
    assert np.isclose(noise_diff.std(), 0.2 * df['feature'].std(), atol=1), "Injected noise should match the specified intensity"

def test_uniform_noise_injection():
    df = pd.DataFrame({'feature': np.random.uniform(20, 80, 1000)})
    injector = NoiseInjector(noise_percentage=0.1, noise_intensity=0.2, random_seed=42)
    noisy_df = injector.inject_noise(df, columns=['feature'], noise_type="uniform")

    # Check that roughly 10% of rows have been altered
    num_noisy_points = int(len(df) * 0.1)
    num_changed = (noisy_df['feature'] != df['feature']).sum()
    assert num_noisy_points * 0.8 <= num_changed <= num_noisy_points * 1.2, "Incorrect number of uniform noise points injected"

    # Verify that noise injection is based on uniform distribution within specified bounds
    noise_diff = noisy_df['feature'] - df['feature']
    range_check = np.all(np.abs(noise_diff) <= 0.2 * (df['feature'].max() - df['feature'].min()))
    assert range_check, "Uniform noise should be within specified bounds based on intensity"

def test_noise_injection_with_default_columns():
    # If no columns specified, inject noise into all numeric columns
    df = pd.DataFrame({
        'feature1': np.random.normal(50, 5, 1000),
        'feature2': np.random.uniform(20, 80, 1000),
        'category': np.random.choice(['A', 'B', 'C'], 1000)
    })
    injector = NoiseInjector(noise_percentage=0.1, noise_intensity=0.2, random_seed=42)
    noisy_df = injector.inject_noise(df, noise_type="gaussian")

    # Check that only numeric columns were affected
    assert noisy_df['category'].equals(df['category']), "Non-numeric columns should not be affected"

    # Check that numeric columns have noise injected
    for col in ['feature1', 'feature2']:
        num_noisy_points = int(len(df) * 0.1)
        num_changed = (noisy_df[col] != df[col]).sum()
        assert num_noisy_points * 0.8 <= num_changed <= num_noisy_points * 1.2, f"Incorrect number of noise points injected in {col}"

def test_no_noise_when_percentage_zero():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = NoiseInjector(noise_percentage=0.0, noise_intensity=0.2, random_seed=42)
    noisy_df = injector.inject_noise(df, columns=['feature'], noise_type="gaussian")

    # Check that no noise was injected
    assert noisy_df.equals(df), "DataFrame should be unchanged when noise percentage is zero"

def test_random_seed_reproducibility():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})

    # Inject noise with the same seed twice and verify they produce the same result
    injector1 = NoiseInjector(noise_percentage=0.1, noise_intensity=0.2, random_seed=42)
    injector2 = NoiseInjector(noise_percentage=0.1, noise_intensity=0.2, random_seed=42)

    noisy_df1 = injector1.inject_noise(df, columns=['feature'], noise_type="gaussian")
    noisy_df2 = injector2.inject_noise(df, columns=['feature'], noise_type="gaussian")

    assert noisy_df1.equals(noisy_df2), "Noise injection should be reproducible with the same random seed"
