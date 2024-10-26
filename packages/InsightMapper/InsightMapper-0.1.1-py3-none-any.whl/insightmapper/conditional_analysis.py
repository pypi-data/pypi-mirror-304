import pandas as pd
from sklearn.feature_selection import mutual_info_regression

class ConditionalAnalyzer:
    def __init__(self, dataframe):
        self.dataframe = dataframe

    def conditional_dependency(self, target, conditional_on):
        """Calculates dependency of a target feature conditioned on another feature."""
        results = {}
        unique_conditions = self.dataframe[conditional_on].unique()

        for condition in unique_conditions:
            subset = self.dataframe[self.dataframe[conditional_on] == condition]
            if len(subset) > 1:
                dependency_score = mutual_info_regression(
                    subset[target].values.reshape(-1, 1),
                    subset.drop(columns=[target, conditional_on])
                ).mean()
                results[condition] = dependency_score

        return results
