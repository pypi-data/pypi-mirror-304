import unittest
import pandas as pd
from insightmapper.dependency_map import DependencyMap
from insightmapper.visualization import DependencyVisualizer

class TestDependencyVisualizer(unittest.TestCase):
    def test_plot_dependency_map(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6], "C": [7, 8, 9]})
        dep_map = DependencyMap(df)
        dependency_matrix = dep_map.compute_dependencies()
        visualizer = DependencyVisualizer(dependency_matrix)
        visualizer.plot_dependency_map(threshold=0.1)

if __name__ == "__main__":
    unittest.main()
