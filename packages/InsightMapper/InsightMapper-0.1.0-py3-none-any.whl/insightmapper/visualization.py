import networkx as nx
import matplotlib.pyplot as plt

class DependencyVisualizer:
    def __init__(self, dependency_matrix):
        self.dependency_matrix = dependency_matrix

    def plot_dependency_map(self, threshold=0.1):
        """Plots a network graph of dependencies with edges based on a threshold."""
        G = nx.Graph()

        for col_x in self.dependency_matrix.columns:
            for col_y in self.dependency_matrix.index:
                if col_x != col_y and self.dependency_matrix.loc[col_x, col_y] > threshold:
                    G.add_edge(col_x, col_y, weight=self.dependency_matrix.loc[col_x, col_y])

        pos = nx.spring_layout(G, k=0.15, seed=42)
        edges = G.edges(data=True)
        weights = [edge[2]['weight'] for edge in edges]
        nx.draw(G, pos, with_labels=True, width=weights, node_size=500, node_color="skyblue")
        plt.show()
