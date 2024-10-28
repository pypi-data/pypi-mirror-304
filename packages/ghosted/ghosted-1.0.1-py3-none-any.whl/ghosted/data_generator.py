import numpy as np
import pandas as pd
from ghosted.synth_dataframe import SynthDataFrame

class DataGenerator:
    def __init__(self):
        pass

    def apply_rounding(self, data, round_param):
        """
        Apply rounding to the generated data if specified.

        Parameters:
            data (np.array): Array of generated synthetic data.
            round_param (int or None): If specified, round data to this number of decimals or to integers.
        
        Returns:
            np.array: Rounded data.
        """
        if round_param is not None:
            rounded_data = np.round(data, round_param)
            if round_param == 0:
                return rounded_data.astype(int)
            return rounded_data
        return data

    def ensure_positive_only(self, data):
        """
        Ensure the data contains only positive values by transforming negative values.
        
        Parameters:
            data (np.array): Generated synthetic data.
        
        Returns:
            np.array: Data with negative values replaced or filtered to be non-negative.
        """
        return np.where(data < 0, 0, data) 

    def generate_column(self, col_spec, num_samples):
        """
        Generate synthetic data for a single column based on the column specification.

        Parameters:
            col_spec (dict): Specifications for the column (distribution, parameters, etc.).
            num_samples (int): Number of samples to generate.

        Returns:
            np.array: Array of generated synthetic data for the column.
        """
        dist_type = col_spec['distribution']
        round_param = col_spec.get('round', None) 
        positive_only = col_spec.get('positive_only', False)
        
        if dist_type == 'uniform':
            required_arguments = ['min', 'max']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for uniform distribution: {missing_arguments}")
            data = np.random.uniform(col_spec['min'], col_spec['max'], num_samples)
        
        elif dist_type == 'normal':
            required_arguments = ['mean', 'std']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for normal distribution: {missing_arguments}")
            data = np.random.normal(col_spec['mean'], col_spec['std'], num_samples)

        elif dist_type == 'binomial':
            required_arguments = ['n', 'p']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for binomial distribution: {missing_arguments}")
            data = np.random.binomial(col_spec['n'], col_spec['p'], num_samples)

        elif dist_type == 'poisson':
            required_arguments = ['lambda']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing argument for poisson distribution: {missing_arguments}")
            data = np.random.poisson(col_spec['lambda'], num_samples)

        elif dist_type == 'geometric':
            required_arguments = ['p']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing argument for geometric distribution: {missing_arguments}")
            data = np.random.geometric(col_spec['p'], num_samples)

        elif dist_type == 'exponential':
            required_arguments = ['lambda']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing argument for exponential distribution: {missing_arguments}")
            data = np.random.exponential(1 / col_spec['lambda'], num_samples)

        elif dist_type == 'categorical':
            required_arguments = ['categories', 'probabilities']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for categorical distribution: {missing_arguments}")
            return np.random.choice(col_spec['categories'], size=num_samples, p=col_spec.get('probabilities'))

        elif dist_type == 'lognormal':
            required_arguments = ['mean', 'std']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for lognormal distribution: {missing_arguments}")
            data = np.random.lognormal(col_spec['mean'], col_spec['std'], num_samples)

        elif dist_type == 'beta':
            required_arguments = ['alpha', 'beta']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for beta distribution: {missing_arguments}")
            data = np.random.beta(col_spec['alpha'], col_spec['beta'], num_samples)

        elif dist_type == 'gamma':
            required_arguments = ['shape', 'rate']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for gamma distribution: {missing_arguments}")
            data = np.random.gamma(col_spec['shape'], col_spec['rate'], num_samples)

        elif dist_type == 'pareto':
            required_arguments = ['shape']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing argument for pareto distribution: {missing_arguments}")
            data = np.random.pareto(col_spec['shape'], num_samples)

        elif dist_type == 'weibull':
            required_arguments = ['shape', 'scale']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for weibull distribution: {missing_arguments}")
            data = np.random.weibull(col_spec['shape'], num_samples) * col_spec['scale']

        elif dist_type == 'triangular':
            required_arguments = ['low', 'mode', 'high']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for triangular distribution: {missing_arguments}")
            data = np.random.triangular(col_spec['low'], col_spec['mode'], col_spec['high'], num_samples)

        elif dist_type == 'bernoulli':
            required_arguments = ['p']
            missing_arguments = [x for x in required_arguments if x not in col_spec.keys()]
            if missing_arguments:
                raise ValueError(f"Missing arguments for bernoulli distribution: {missing_arguments}")
            data = np.random.binomial(1, col_spec['p'], num_samples)

        else:
            raise ValueError(f"Unknown distribution type: {dist_type}")

        if positive_only:
            data = self.ensure_positive_only(data)

        return self.apply_rounding(data, round_param)

    def generate_synthetic_data(self, column_spec, num_samples=100, random_seed=None):
        """
        Generate synthetic data for all columns based on the user-defined specifications.

        Parameters:
            column_spec (dict): Dictionary with column names as keys and distribution specs as values.
            num_samples (int): Number of samples to generate.

        Returns:
            pd.DataFrame: DataFrame containing the generated synthetic data.
        """
        data = {}
        for col_name, col_spec in column_spec.items():
            data[col_name] = self.generate_column(col_spec, num_samples)

            if col_spec['distribution'] == 'categorical':
                data[col_name] = pd.Categorical(data[col_name], categories=col_spec['categories'])

        df = pd.DataFrame(data)
        synthetic_df = SynthDataFrame(data, random_seed=random_seed)
        synthetic_df['synthetic_flag'] = 1
        return synthetic_df
