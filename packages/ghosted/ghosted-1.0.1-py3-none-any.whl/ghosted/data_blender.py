import numpy as np
import pandas as pd
from scipy import stats
from ghosted.data_generator import DataGenerator
from ghosted.synth_dataframe import SynthDataFrame
from copulas.multivariate import GaussianMultivariate
from scipy.stats import pearsonr

class DataBlender:
    def __init__(self):
        self.generator = DataGenerator()

    def detect_rounding(self, column_data):
        """
        Detect if the input data is rounded to integers or specific decimal places.
        Returns the number of decimal places the data appears to be rounded to.
        """
        if pd.api.types.is_integer_dtype(column_data):
            return 0
        elif pd.api.types.is_float_dtype(column_data):
            try:
                decimal_places = column_data.apply(lambda x: len(str(x).split(".")[1]) if "." in str(x) else 0)
                if decimal_places.mode()[0] > 15:
                    return None
                return decimal_places.mode()[0]
            except (ValueError, IndexError):
                return None
        return None

    def detect_distribution(self, column_data):
        """
        Detect the most appropriate distribution for a given column of data.
        """
        rounding = self.detect_rounding(column_data)

        if column_data.dtype == 'object' or column_data.nunique() / len(column_data) < 0.05:
            value_counts = column_data.value_counts(normalize=True)
            return 'categorical', value_counts.index.tolist(), value_counts.values.tolist(), rounding

        if column_data.min() >= 0 and column_data.max() <= 1:
            alpha, beta, _, _ = stats.beta.fit(column_data, floc=0, fscale=1)
            return 'beta', {'alpha': alpha, 'beta': beta}, rounding

        # Fit Normal distribution
        mean, std = column_data.mean(), column_data.std()
        normal_p_value = stats.kstest(column_data, 'norm', args=(mean, std)).pvalue
        skewness = stats.skew(column_data)
        kurtosis = stats.kurtosis(column_data)

        # Fit Exponential distribution (for skewed positive data)
        if column_data.min() >= 0:
            loc, scale = stats.expon.fit(column_data)
            exp_p_value = stats.kstest(column_data, 'expon', args=(loc, scale)).pvalue

            # Fit Gamma distribution for non-negative values
            if column_data.min() > 0:
                shape, loc, scale = stats.gamma.fit(column_data, floc=0)
                gamma_p_value = stats.kstest(column_data, 'gamma', args=(shape, loc, scale)).pvalue

                if np.isclose(shape, 1, atol=0.3) and exp_p_value > 0.15:
                    return 'exponential', {'lambda': 1 / scale}, rounding

                if normal_p_value > 0.05 and abs(skewness) < 0.5 and abs(kurtosis) < 3:
                    return 'normal', {'mean': mean, 'std': std}, rounding
                elif gamma_p_value > exp_p_value:
                    return 'gamma', {'shape': shape, 'rate': 1 / scale}, rounding

        # Default to uniform distribution if no specific distribution is detected
        min_val, max_val = column_data.min(), column_data.max()
        return 'uniform', {'min': min_val, 'max': max_val}, rounding


    def generate_additional_data(self, col_name, col_spec, existing_data, num_samples):
        """
        Generate new data points based on the detected distribution for each column.
        Applies the same rounding as the original data, if applicable.
        """
        rounding = col_spec[2]
        
        if col_spec[0] == 'categorical':
            categories = col_spec[1]
            probabilities = col_spec[2]
            return np.random.choice(categories, size=num_samples, p=probabilities)
        
        elif col_spec[0] == 'normal':
            col_spec_dict = {'distribution': 'normal', 'mean': col_spec[1]['mean'], 'std': col_spec[1]['std']}
            new_data = self.generator.generate_column(col_spec_dict, num_samples)
        
        elif col_spec[0] == 'exponential':
            col_spec_dict = {'distribution': 'exponential', 'lambda': col_spec[1]['lambda']}
            new_data = self.generator.generate_column(col_spec_dict, num_samples)
            new_data = np.clip(new_data, 0, None)
        
        elif col_spec[0] == 'beta':
            col_spec_dict = {'distribution': 'beta', 'alpha': col_spec[1]['alpha'], 'beta': col_spec[1]['beta']}
            new_data = self.generator.generate_column(col_spec_dict, num_samples)
            new_data = np.clip(new_data, 0, 1)

        elif col_spec[0] == 'gamma':
            col_spec_dict = {'distribution': 'gamma', 'shape': col_spec[1]['shape'], 'rate': col_spec[1]['rate']}
            new_data = self.generator.generate_column(col_spec_dict, num_samples)
            new_data = np.clip(new_data, 0, None)

        elif col_spec[0] == 'uniform':
            col_spec_dict = {'distribution': 'uniform', 'min': col_spec[1]['min'], 'max': col_spec[1]['max']}
            new_data = self.generator.generate_column(col_spec_dict, num_samples)
        
        if rounding is not None:
            new_data = np.round(new_data, rounding)
            if rounding == 0:
                return new_data.astype(int)
        return new_data


    def blend_data(self, df, num_samples, random_seed=None):
        """
        Blend data by generating additional samples for each column in the dataframe.

        Parameters:
            df (pd.DataFrame): The original dataframe.
            num_samples (int): Number of additional samples to generate.

        Returns:
            SynthDataFrame: A new dataframe containing the original and additional samples with a synthetic_flag.
        """
        new_data = {}

        for col_name in df.columns:
            col_data = df[col_name]
            col_spec = self.detect_distribution(col_data)
            new_col_data = self.generate_additional_data(col_name, col_spec, col_data, num_samples)

            if isinstance(col_data.dtype, pd.CategoricalDtype) or df[col_name].dtype == object:
                col_data = pd.Categorical(col_data, categories=col_data.unique())
                new_col_data = pd.Categorical(new_col_data, categories=col_data.categories)
                
                new_data[col_name] = pd.concat([pd.Series(col_data), pd.Series(new_col_data)])
            else:
                new_data[col_name] = np.concatenate([col_data.values, new_col_data])

        real_and_synthetic_df = pd.DataFrame(new_data)

        blended_df = SynthDataFrame(real_and_synthetic_df, random_seed=random_seed)

        synthetic_flag = [0] * len(df) + [1] * num_samples  # Correct the length for synthetic data
        blended_df['synthetic_flag'] = synthetic_flag

        return blended_df
    
    def blend_data_with_correlation(self, df, num_samples, columns_with_correlation=None):
        """
        Blend data by generating additional samples with preserved correlations for specified columns.

        Parameters:
            df (pd.DataFrame): The original dataframe.
            num_samples (int): Number of additional samples to generate.
            columns_with_correlation (list of str): Columns to preserve correlation. If None, uses all columns.

        Returns:
            pd.DataFrame: A new dataframe containing the original and additional samples with correlations preserved.
        """
        if columns_with_correlation is None:
            columns_with_correlation = df.columns

        copula = GaussianMultivariate()
        copula.fit(df[columns_with_correlation])

        synthetic_data = copula.sample(num_samples)
        synthetic_data['synthetic_flag'] = 1

        real_data = df.copy()
        real_data['synthetic_flag'] = 0

        blended_df = pd.concat([real_data, synthetic_data], ignore_index=True)

        return SynthDataFrame(blended_df)

    def replace_data(self, df, num_samples=None, random_seed=None, columns_with_correlation=None):
        """
        Replace real data with fully synthetic data based on the distributions of the original data.

        Parameters:
            df (pd.DataFrame): The original dataframe.
            num_samples (int): Number of synthetic samples to generate. Defaults to the number of rows in the original data.
            random_seed (int): Optional random seed for reproducibility.
            columns_with_correlation (list of str): List of columns with pairwise correlation to preserve.
        
        Returns:
            SynthDataFrame: A fully synthetic dataframe with distributions mimicking the original data.
        """
        if random_seed is not None:
            np.random.seed(random_seed)

        if num_samples is None:
            num_samples = len(df)

        synthetic_data = {}

        for col_name in df.columns:
            col_data = df[col_name]
            col_spec = self.detect_distribution(col_data)

            synthetic_data[col_name] = self.generate_additional_data(col_name, col_spec, col_data, num_samples)

        synthetic_df = SynthDataFrame(synthetic_data, random_seed=random_seed)
        synthetic_df['synthetic_flag'] = 1

        if columns_with_correlation:
            for i in range(len(columns_with_correlation) - 1):
                primary_col = columns_with_correlation[i]
                correlated_col = columns_with_correlation[i + 1]
                self._preserve_pairwise_correlation(
                    synthetic_df, primary_col, correlated_col
                )

        return synthetic_df

    def _preserve_pairwise_correlation(self, synthetic_df, primary_col, correlated_col):
        """
        Adjusts the values in correlated_col of synthetic_df to have a similar correlation 
        with primary_col as in the original data.
        """
        synthetic_corr = synthetic_df[[primary_col, correlated_col]].corr().iloc[0, 1]
        
        orig_corr, _ = pearsonr(synthetic_df[primary_col], synthetic_df[correlated_col])
        
        synthetic_df[correlated_col] = synthetic_df[primary_col] * (orig_corr / synthetic_corr) \
                                       + synthetic_df[correlated_col] * (1 - orig_corr / synthetic_corr)