import numpy as np
import pandas as pd

class NoiseInjector:
    def __init__(self, noise_percentage=0.1, noise_intensity=0.2, random_seed=None):
        self.noise_percentage = noise_percentage
        self.noise_intensity = noise_intensity
        self.random_seed = random_seed
        self.random_state = np.random.RandomState(random_seed)

    def inject_noise(self, df, columns=None, noise_type="gaussian"):
        if columns is None:
            columns = df.select_dtypes(include=np.number).columns

        df_noisy = df.copy()
        num_rows = len(df)

        for col in columns:
            num_noisy_points = int(num_rows * self.noise_percentage)
            noisy_indices = self.random_state.choice(num_rows, num_noisy_points, replace=False)

            if noise_type == "gaussian":
                std_dev = df[col].std()
                noise = self.random_state.normal(0, self.noise_intensity * std_dev, num_noisy_points)
                df_noisy.loc[noisy_indices, col] += noise

            elif noise_type == "uniform":
                data_range = df[col].max() - df[col].min()
                noise = self.random_state.uniform(-self.noise_intensity * data_range,
                                                  self.noise_intensity * data_range,
                                                  num_noisy_points)
                df_noisy.loc[noisy_indices, col] += noise

        return df_noisy
