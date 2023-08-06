"""
Python module for UMAP visualization
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import plotly
import plotly.express as px
import umap
from joblib import Parallel, delayed
from umap.parametric_umap import ParametricUMAP


class UMAPVisualization :
    """
    UMAPVisualization class provides different visualizations of high dimensional data
    using UMAP embedding.

    Parameters:
    data (numpy.ndarray): High dimensional data.
    n_components (int): Number of dimensions to reduce to.
    n_neighbors (int): Number of nearest neighbors to use in UMAP model.
    min_dist (float): The minimum distance between embedded points.
    """
    def __init__(self, data:np.ndarray, n_components: int = 2, n_neighbors: int = 15,
                 min_dist: float = 0.2, parametric: bool = False) :
        self.data = data
        self.n_components = n_components
        self.n_neighbors = n_neighbors
        self.min_dist = min_dist
        self.parametric = parametric
        if parametric :
            self.umap_model = ParametricUMAP (n_components=n_components,
                                              n_neighbors=n_neighbors,
                                              min_dist=min_dist,
                                              n_epochs=50,
                                              verbose=True)
        else:
            self.umap_model = umap.UMAP(n_components=n_components,
                                         n_neighbors=n_neighbors,
                                         min_dist=min_dist)

        self.embedding = self.umap_model.fit_transform (self.data)


    def scatter_plot(self, labels:np.ndarray=None) -> plotly.graph_objects.Figure :
        """
        Plot the UMAP scatter plot of the data.

        Parameters:
        labels (list): List of labels corresponding to each data point.
        cmap (str): Colormap to use in the plot.
        """
        plot_data = pd.DataFrame(self.embedding)
        plot_data.columns = ["umap_" + str(col+1) for col in plot_data.columns]
        plot_data['labels'] = labels

        if self.n_components == 2 :
            fig = px.scatter(plot_data, x="umap_1", y="umap_2", color="labels")
        elif self.n_components >= 3:
            fig = px.scatter_3d(plot_data, x="umap_1", y="umap_2", z="umap_3", color="labels")
        else:
            raise Exception("The number of components for umap should be greater than or equal to two")
        return fig

    @staticmethod
    def compute_umap(min_dist: float, n_neighbor: int, data: np.ndarray, parametric:bool) -> pd.DataFrame :
        """
        Static method to compute umap projections
        """
        try:
            print ("Computing UMAP for {} and {}".format (n_neighbor, min_dist))
            if parametric:
                umap_model = ParametricUMAP(n_neighbors=n_neighbor, min_dist=min_dist)
            else:
                umap_model = umap.UMAP (n_neighbors=n_neighbor, min_dist=min_dist)
            umap_data = pd.DataFrame (umap_model.fit_transform (data))
            umap_data.columns = ["umap_1", "umap_2"]
            umap_data['min_dist'] = min_dist
            umap_data['n_neighbor'] = n_neighbor
            return umap_data
        except Exception as e:
            print ("Error while computing UMAP for {} and {}: {}".format (n_neighbor, min_dist, str(e)))
            return pd.DataFrame ()

    def plot_min_dist_vs_n_neighbors (self, data: np.ndarray, min_dists: list, n_neighbors: list, labels: np.ndarray,
                                      parametric:bool=False) -> (pd.DataFrame, plotly.graph_objects.Figure):
        """
        Plot the UMAP scatter plot for different combinations of min_dist and n_neighbors.

        Parameters:
        data (numpy.ndarray): High dimensional data.
        min_dists (list): List of min_dists to try.
        n_neighbors (list): List of n_neighbors to try.
        labels (list): List of labels corresponding to each data point.
        """
        try:
            results = pd.concat (Parallel (n_jobs=-1) (
                delayed (UMAPVisualization.compute_umap) (min_dist, n_neighbor, data, parametric)
                for min_dist in min_dists for n_neighbor in n_neighbors
            ), axis=0)

            results['label'] = np.tile(labels, len (min_dists) * len (n_neighbors))

            fig = px.scatter(results, x="umap_1", y="umap_2", color="label", facet_row="n_neighbor", facet_col="min_dist")

            return results, fig
        except Exception as e:
            print ("Error creating the chart: {}".format (str (e)))
            return pd.DataFrame(), px.scatter()
