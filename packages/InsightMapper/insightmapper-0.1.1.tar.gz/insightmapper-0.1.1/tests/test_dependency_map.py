import unittest
import pandas as pd
from insightmapper.dependency_map import DependencyMap

class TestDependencyMap(unittest.TestCase):
    def test_compute_dependencies(self):
        df = pd.DataFrame({"A": [1, 2, 3], "B": [4, 5, 6]})
        dep_map = DependencyMap(df)
        dependency_matrix = dep_map.compute_dependencies()
        self.assertTrue((dependency_matrix.values.diagonal() == 1.0).all())

if __name__ == "__main__":
    unittest.main()
