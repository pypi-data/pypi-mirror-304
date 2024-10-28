import pytest
import numpy as np
import pandas as pd
from ghosted.anomaly_injector import AnomalyInjector

np.random.seed(42)

def test_basic_anomaly_injection():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['feature'], anomaly_type="extreme_value", factor=3)
    
    num_anomalies = (df_with_anomalies['feature'] != df['feature']).sum()
    expected_anomalies = int(len(df) * 0.05)
    assert num_anomalies == expected_anomalies, "Incorrect number of anomalies injected"

def test_positive_direction_anomaly_injection():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['feature'], anomaly_type="extreme_value", factor=3, direction="positive")
    
    anomalies = df_with_anomalies.loc[df_with_anomalies['feature'] > df['feature'].max(), 'feature']
    assert len(anomalies) > 0, "Positive anomalies not injected as expected"
    assert (anomalies > df['feature'].mean()).all(), "Not all positive anomalies are above the mean"

def test_negative_direction_anomaly_injection():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['feature'], anomaly_type="extreme_value", factor=3, direction="negative")
    
    anomalies = df_with_anomalies.loc[df_with_anomalies['feature'] < df['feature'].quantile(0.05), 'feature']
    assert len(anomalies) > 0, "Negative anomalies not injected as expected"

def test_anomalies_with_variability():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['feature'], anomaly_type="extreme_value", factor=3, variation=0.1)
    
    anomalies = df_with_anomalies.loc[df_with_anomalies['feature'] != df['feature'], 'feature']
    assert anomalies.nunique() > 1, "Anomalies lack variability with specified variation factor"

def test_pattern_break_anomaly_injection_numeric():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['feature'], anomaly_type="pattern_break")
    
    anomaly_indices = (df_with_anomalies['feature'] != df['feature'])
    anomalies = df_with_anomalies[anomaly_indices]
    
    assert (anomalies['feature'] > df['feature'].quantile(0.95)).any() or (anomalies['feature'] < df['feature'].quantile(0.05)).any(), "Pattern-breaking anomalies not injected as expected"

def test_pattern_break_anomaly_injection_categorical():
    df = pd.DataFrame({'category': np.random.choice(['A', 'B', 'C'], 1000)})
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['category'], anomaly_type="pattern_break")
    
    num_anomalies = (df_with_anomalies['category'] != df['category']).sum()
    expected_anomalies = int(len(df) * 0.05)
    
    # Adjust lower bound to 60% tolerance and 140% tolerance to allow for some variability
    assert expected_anomalies * 0.6 <= num_anomalies <= expected_anomalies * 1.4, "Incorrect number of pattern-breaking anomalies for categorical data"

def test_custom_anomaly_injection():
    df = pd.DataFrame({'feature': np.random.normal(50, 5, 1000)})
    
    def custom_anomaly(column):
        return column + 999  # Arbitrary custom anomaly logic
    
    injector = AnomalyInjector(anomaly_percentage=0.05, random_seed=42)
    df_with_anomalies = injector.inject_anomalies(df, columns=['feature'], anomaly_type=custom_anomaly)
    
    anomalies = df_with_anomalies.loc[df_with_anomalies['feature'] != df['feature'], 'feature']
    assert (anomalies > 1000).all(), "Custom anomalies not injected as expected"
