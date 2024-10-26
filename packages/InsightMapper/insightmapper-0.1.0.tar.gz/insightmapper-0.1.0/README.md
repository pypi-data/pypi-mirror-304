# InsightMapper

InsightMapper is a Python package for mapping and visualizing dependencies between variables in complex datasets.

## Features

- Non-linear dependency detection
- Conditional dependency analysis
- Interactive dependency maps
- Influence ranking of features

## Installation

To install, use:

```bash
pip install InsightMapper
```

## Usage
### Basic Dependency Mapping
#### Use InsightMapper to create a dependency matrix that highlights relationships between variables.
```bash
from insightmapper import DependencyMap
import pandas as pd

# Sample DataFrame
df = pd.DataFrame({
    'A': [1, 2, 3, 4, 5],
    'B': [2, 3, 4, 5, 6],
    'C': [5, 4, 3, 2, 1],
})

# Initialize DependencyMap and compute dependencies
dep_map = DependencyMap(df)
dependency_matrix = dep_map.compute_dependencies()

print("Dependency Matrix:\n", dependency_matrix)

# Get top influential features
top_influencers = dep_map.get_most_influential_features(top_n=3)
print("Top Influential Features:\n", top_influencers)
```

### Conditional Dependency Analysis
#### Analyze how the dependency of one variable changes when conditioned on another variable.

```bash
from insightmapper import ConditionalAnalyzer

cond_analyzer = ConditionalAnalyzer(df)
conditional_dependency = cond_analyzer.conditional_dependency(target="A", conditional_on="B")
print("Conditional Dependency:\n", conditional_dependency)
```

### Visualizing the Dependency Map
#### Visualize the dependency matrix as an interactive network graph.

```bash
from insightmapper import DependencyVisualizer

# Initialize the visualizer with the computed dependency matrix
visualizer = DependencyVisualizer(dependency_matrix)
visualizer.plot_dependency_map(threshold=0.1)
```