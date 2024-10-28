import numpy as np
import pandas as pd

class AnomalyInjector:
    def __init__(self, anomaly_percentage=0.05, random_seed=None):
        """
        Initialize the AnomalyInjector.

        Parameters:
            anomaly_percentage (float): Default percentage of rows to inject anomalies into.
            random_seed (int, optional): Set a random seed for reproducibility.
        """
        self.anomaly_percentage = anomaly_percentage
        self.random_seed = random_seed
        if random_seed is not None:
            np.random.seed(random_seed)
    
    def inject_anomalies(self, df, columns, anomaly_type="extreme_value", factor=3, direction="both", variation=0.1):
        """
        Inject anomalies into specified columns of the dataframe.

        Parameters:
            df (pd.DataFrame): The original dataframe.
            columns (list of str): List of columns to inject anomalies into.
            anomaly_type (str): Type of anomaly to inject. Options: "extreme_value", "pattern_break", or "custom".
            factor (float): Factor by which to scale extreme values, used for extreme_value anomalies.
            direction (str): Direction of extreme values for "extreme_value" anomalies. 
                             Options are "both", "positive", or "negative".
            variation (float): Amount of random variation to add to each anomaly for more realistic anomalies.

        Returns:
            pd.DataFrame: DataFrame with injected anomalies.
        """
        df_with_anomalies = df.copy()
        num_anomalies = int(len(df) * self.anomaly_percentage)

        for col in columns:
            if col not in df_with_anomalies.columns:
                raise ValueError(f"Column '{col}' not found in the dataframe.")
                
            anomaly_indices = np.random.choice(df_with_anomalies.index, num_anomalies, replace=False)
            
            if anomaly_type == "extreme_value":
                mean, std = df_with_anomalies[col].mean(), df_with_anomalies[col].std()
                
                if direction == "positive":
                    anomalies = mean + factor * std + np.random.normal(0, std * variation, num_anomalies)
                elif direction == "negative":
                    anomalies = mean - factor * std + np.random.normal(0, std * variation, num_anomalies)
                elif direction == "both":
                    signs = np.random.choice([-1, 1], size=num_anomalies)
                    anomalies = mean + factor * std * signs + np.random.normal(0, std * variation, num_anomalies)
                else:
                    raise ValueError("Direction must be 'both', 'positive', or 'negative'")
                
                df_with_anomalies.loc[anomaly_indices, col] = anomalies
            
            elif anomaly_type == "pattern_break":
                if pd.api.types.is_numeric_dtype(df_with_anomalies[col]):
                    df_with_anomalies.loc[anomaly_indices, col] = np.random.uniform(
                        df_with_anomalies[col].min() * 1.5, 
                        df_with_anomalies[col].max() * 1.5, 
                        size=num_anomalies
                    )
                else:
                    unique_values = df_with_anomalies[col].unique()
                    df_with_anomalies.loc[anomaly_indices, col] = np.random.choice(unique_values, size=num_anomalies)
            
            elif callable(anomaly_type):
                df_with_anomalies.loc[anomaly_indices, col] = anomaly_type(df_with_anomalies[col].iloc[anomaly_indices])
            
            else:
                raise ValueError(f"Anomaly type '{anomaly_type}' is not recognized.")

        return df_with_anomalies
