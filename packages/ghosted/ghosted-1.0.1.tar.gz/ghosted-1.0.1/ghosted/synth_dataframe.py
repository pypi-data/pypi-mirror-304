import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np

class SynthDataFrame(pd.DataFrame):
    _metadata = ['random_seed']

    def __init__(self, *args, **kwargs):
        self.random_seed = kwargs.pop('random_seed', None)
        if self.random_seed is not None:
            np.random.seed(self.random_seed)
        super().__init__(*args, **kwargs)

    @property
    def _constructor(self):
        return SynthDataFrame

    def summarize(self):
        numeric_cols = [col for col in self.columns if pd.api.types.is_numeric_dtype(self[col]) and col != 'synthetic_flag']
        categorical_cols = [col for col in self.columns if pd.api.types.is_categorical_dtype(self[col]) or self[col].dtype == object]
        
        # Numeric Summary
        if numeric_cols:
            summary_rows = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
            numeric_summary = pd.DataFrame(index=summary_rows)

            for col in numeric_cols:
                real_data = self[self['synthetic_flag'] == 0][col]
                synthetic_data = self[self['synthetic_flag'] == 1][col]

                numeric_summary[f"{col}_real"] = [
                    real_data.count(), real_data.mean(), real_data.std(), real_data.min(),
                    real_data.quantile(0.25), real_data.median(), real_data.quantile(0.75), real_data.max()
                ]
                numeric_summary[f"{col}_synthetic"] = [
                    synthetic_data.count(), synthetic_data.mean(), synthetic_data.std(), synthetic_data.min(),
                    synthetic_data.quantile(0.25), synthetic_data.median(), synthetic_data.quantile(0.75), synthetic_data.max()
                ]
            
            print("\nNumeric Data Summary:")
            print(numeric_summary)

        # Categorical Summary
        if categorical_cols:
            categorical_summary = []
            for col in categorical_cols:
                real_data = self[self['synthetic_flag'] == 0][col]
                synthetic_data = self[self['synthetic_flag'] == 1][col]
                
                all_categories = pd.concat([real_data, synthetic_data]).unique()

                real_counts = real_data.value_counts().reindex(all_categories, fill_value=0)
                synthetic_counts = synthetic_data.value_counts().reindex(all_categories, fill_value=0)

                cat_summary = pd.DataFrame({
                    'Feature': col,
                    'Label': all_categories,
                    'Real Data Count': real_counts.values,
                    'Synthetic Data Count': synthetic_counts.values
                })

                categorical_summary.append(cat_summary)

            categorical_summary_df = pd.concat(categorical_summary, ignore_index=True)

            print("\nCategorical Data Summary:")
            print(categorical_summary_df.to_string(index=False))

    def visualize(self, column=None, kind="kde"):
        if column:
            if pd.api.types.is_numeric_dtype(self[column]):
                plt.figure(figsize=(8, 6))

                real_data = self[self['synthetic_flag'] == 0][column]
                synthetic_data = self[self['synthetic_flag'] == 1][column]

                fig, ax1 = plt.subplots(figsize=(8, 6))

                if len(real_data) > 0 and len(synthetic_data) > 0:
                    if kind == "kde":
                        sns.kdeplot(real_data, ax=ax1, color='tab:blue', fill=False, label='Real Data')
                        ax1.set_ylabel('Real Data Density', color='tab:blue')
                    else:
                        ax1.hist(real_data, bins=30, color='tab:blue', alpha=0.5, label='Real Data')
                        ax1.set_ylabel('Real Data Count', color='tab:blue')

                    ax1.tick_params(axis='y', labelcolor='tab:blue')

                    ax2 = ax1.twinx()
                    if kind == "kde":
                        sns.kdeplot(synthetic_data, ax=ax2, color='tab:red', fill=False, label='Synthetic Data')
                        ax2.set_ylabel('Synthetic Data Density', color='tab:red')
                    else:
                        ax2.hist(synthetic_data, bins=30, color='tab:red', alpha=0.5, label='Synthetic Data')
                        ax2.set_ylabel('Synthetic Data Count', color='tab:red')

                    ax2.tick_params(axis='y', labelcolor='tab:red')
                else:
                    if len(real_data) > 0:
                        sns.kdeplot(real_data, ax=ax1, color='tab:blue', fill=False, label='Real Data')
                        ax1.set_ylabel('Real Data Density' if kind == "kde" else 'Real Data Count', color='tab:blue')
                    elif len(synthetic_data) > 0:
                        sns.kdeplot(synthetic_data, ax=ax1, color='tab:red', fill=False, label='Synthetic Data')
                        ax1.set_ylabel('Synthetic Data Density' if kind == "kde" else 'Synthetic Data Count', color='tab:red')

                plt.title(f'{column.capitalize()}')
                plt.show()

            elif pd.api.types.is_categorical_dtype(self[column]) or self[column].dtype == object:
                real_data = self[self['synthetic_flag'] == 0][column]
                synthetic_data = self[self['synthetic_flag'] == 1][column]

                real_counts = real_data.value_counts(normalize=True)
                synthetic_counts = synthetic_data.value_counts(normalize=True)

                combined_data = pd.DataFrame({
                    'Real Data': real_counts,
                    'Synthetic Data': synthetic_counts
                }).fillna(0)

                ax = combined_data.plot(kind='bar', figsize=(10, 6), width=0.8, color=['tab:blue', 'tab:red'])

                ax.set_ylabel('Proportion')
                plt.title(f'{column.capitalize()} (Real vs Synthetic)')

                if len(real_data) > 0 and len(synthetic_data) > 0:
                    plt.legend(loc='upper right')
                else:
                    ax.get_legend().remove()

                plt.show()

            else:
                raise ValueError(f"Column '{column}' is not suitable for plotting (not numeric or categorical).")

        else:
            numeric_cols = [col for col in self.columns if pd.api.types.is_numeric_dtype(self[col]) and col != 'synthetic_flag']
            categorical_cols = [col for col in self.columns if pd.api.types.is_categorical_dtype(self[col]) or self[col].dtype == object]

            max_cols = numeric_cols[:10]

            num_plots = len(max_cols) + len(categorical_cols)
            fig, axes = plt.subplots(nrows=(num_plots + 2) // 3, ncols=3, figsize=(15, 5 * ((num_plots + 2) // 3)))
            axes = axes.flatten()

            for i, col in enumerate(max_cols):
                real_data = self[self['synthetic_flag'] == 0][col]
                synthetic_data = self[self['synthetic_flag'] == 1][col]

                ax1 = axes[i]
                if len(real_data) > 0 and len(synthetic_data) > 0:
                    if kind == "kde":
                        sns.kdeplot(real_data, ax=ax1, color='tab:blue', fill=False, label='Real Data')
                        ax1.set_ylabel('Real Data Density', color='tab:blue')
                    else:
                        ax1.hist(real_data, bins=30, color='tab:blue', alpha=0.5, label='Real Data')
                        ax1.set_ylabel('Real Data Count', color='tab:blue')

                    ax1.tick_params(axis='y', labelcolor='tab:blue')

                    ax2 = ax1.twinx()
                    if kind == "kde":
                        sns.kdeplot(synthetic_data, ax=ax2, color='tab:red', fill=False, label='Synthetic Data')
                        ax2.set_ylabel('Synthetic Data Density', color='tab:red')
                    else:
                        ax2.hist(synthetic_data, bins=30, color='tab:red', alpha=0.5, label='Synthetic Data')
                        ax2.set_ylabel('Synthetic Data Count', color='tab:red')

                    ax2.tick_params(axis='y', labelcolor='tab:red')
                else:
                    if len(real_data) > 0:
                        sns.kdeplot(real_data, ax=ax1, color='tab:blue', fill=False, label='Real Data')
                        ax1.set_ylabel('Real Data Density' if kind == "kde" else 'Real Data Count', color='tab:blue')
                    elif len(synthetic_data) > 0:
                        sns.kdeplot(synthetic_data, ax=ax1, color='tab:red', fill=False, label='Synthetic Data')
                        ax1.set_ylabel('Synthetic Data Density' if kind == "kde" else 'Synthetic Data Count', color='tab:red')

                ax1.set_title(f'{col.capitalize()}')

            for j, col in enumerate(categorical_cols, start=len(max_cols)):
                real_data = self[self['synthetic_flag'] == 0][col]
                synthetic_data = self[self['synthetic_flag'] == 1][col]

                real_counts = real_data.value_counts(normalize=True)
                synthetic_counts = synthetic_data.value_counts(normalize=True)

                combined_data = pd.DataFrame({
                    'Real Data': real_counts,
                    'Synthetic Data': synthetic_counts
                }).fillna(0)

                ax = axes[j]
                combined_data.plot(kind='bar', ax=ax, width=0.8, color=['tab:blue', 'tab:red'])

                ax.set_ylabel('Proportion')
                ax.set_title(f'{col.capitalize()}')

                if len(real_data) > 0 and len(synthetic_data) > 0:
                    ax.legend(loc='upper right')
                else:
                    ax.get_legend().remove()

            for k in range(j + 1, len(axes)):
                fig.delaxes(axes[k])

            plt.tight_layout()
            plt.show()
    
    def pairwise_plot(self, kind="scatter"):
        """
        Generate pairwise plots for numeric features to analyze correlations.
        
        Parameters:
            kind (str): Type of plot to create for each pair of features ('scatter' or 'kde').
                        'scatter' plots real and synthetic data as points.
                        'kde' creates kernel density plots for each feature pair.
        """
        numeric_cols = [col for col in self.columns if pd.api.types.is_numeric_dtype(self[col]) and col != 'synthetic_flag']
        
        if len(numeric_cols) < 2:
            raise ValueError("At least two numeric columns are required for pairwise plotting.")
        
        real_data = self[self['synthetic_flag'] == 0]
        synthetic_data = self[self['synthetic_flag'] == 1]
        
        if kind == "scatter":
            combined_data = pd.concat([
                real_data.assign(Data="Real"),
                synthetic_data.assign(Data="Synthetic")
            ])

            sns.pairplot(combined_data, vars=numeric_cols, hue="Data", markers=["o", "s"], plot_kws={'alpha': 0.5})
        
        elif kind == "kde":
            pairgrid = sns.PairGrid(self, vars=numeric_cols)
            
            pairgrid.map_upper(lambda x, y, **kwargs: sns.kdeplot(x, y, **kwargs, cmap="Reds", fill=True, alpha=0.3, label="Synthetic"))
            
            pairgrid.map_lower(lambda x, y, **kwargs: sns.kdeplot(x, y, **kwargs, cmap="Blues", fill=True, alpha=0.3, label="Real"))

            pairgrid.map_diag(lambda x, **kwargs: sns.kdeplot(real_data[x.name], color="tab:blue", **kwargs, fill=True, alpha=0.4))
            pairgrid.map_diag(lambda x, **kwargs: sns.kdeplot(synthetic_data[x.name], color="tab:red", **kwargs, fill=True, alpha=0.4))

            for ax in pairgrid.axes.flatten():
                ax.set_ylabel(ax.get_ylabel(), color="tab:blue")
                ax.set_xlabel(ax.get_xlabel(), color="tab:blue")
                
            plt.legend(labels=["Real", "Synthetic"], loc="best")

        plt.suptitle("Pairwise Plot", y=1.02)
        plt.show()