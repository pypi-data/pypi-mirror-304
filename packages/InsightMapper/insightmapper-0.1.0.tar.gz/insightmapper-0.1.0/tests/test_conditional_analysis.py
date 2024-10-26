import unittest
import pandas as pd
from insightmapper.conditional_analysis import ConditionalAnalyzer

class TestConditionalAnalyzer(unittest.TestCase):
    def test_conditional_dependency(self):
        df = pd.DataFrame({
            "A": [1, 2, 3, 4],
            "B": [1, 1, 2, 2],
            "C": [10, 20, 30, 40]
        })
        analyzer = ConditionalAnalyzer(df)
        result = analyzer.conditional_dependency(target="A", conditional_on="B")
        self.assertIn(1, result)

if __name__ == "__main__":
    unittest.main()
