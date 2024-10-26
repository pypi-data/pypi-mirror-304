import pandas as pd
from sklearn.feature_selection import mutual_info_regression
import numpy as np

class DependencyMap:
    def __init__(self, dataframe):
        self.dataframe = dataframe
        self.dependency_matrix = None

    def compute_dependencies(self):
        """Calculates dependencies between features based on mutual information."""
        cols = self.dataframe.select_dtypes(include=[np.number]).columns
        dependency_matrix = pd.DataFrame(index=cols, columns=cols)

        for col_x in cols:
            x = self.dataframe[col_x]
            for col_y in cols:
                y = self.dataframe[col_y]
                if col_x == col_y:
                    dependency_matrix.loc[col_x, col_y] = 1.0
                else:
                    score = mutual_info_regression(x.values.reshape(-1, 1), y)[0]
                    dependency_matrix.loc[col_x, col_y] = score

        self.dependency_matrix = dependency_matrix
        return dependency_matrix

    def get_most_influential_features(self, top_n=5):
        """Returns the top N most influential features based on summed dependency scores."""
        influence_scores = self.dependency_matrix.sum().sort_values(ascending=False)
        return influence_scores.head(top_n)
