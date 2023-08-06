import numpy as np
import plotly.express as px
from sklearn.decomposition import PCA
from umap import UMAP
from umap.plot import _get_embedding, _nhood_search


def local_dim_3d(umap_object: UMAP, local_variance_threshold: float):
    """
        Calculate approximate local dimension for a 3d data UMAP embedding


        TODO: Add Args
        TODO: Write Unit Tests
    """
    points = _get_embedding(umap_object)

    if points.shape[-1] != 3:
        raise NotImplementedError(
            "the local_dim_3d function only works for data sets of dimension 3"
        )

    highd_indicies, highd_dist = _nhood_search(umap_object, umap_object.n_neighbors)
    data = umap_object._raw_data
    local_dim = np.empty(data.shape[0], dtype=np.int64)
    for i in range(data.shape[0]):
        pca = PCA().fit(data[highd_indicies[i]])
        local_dim[i] = np.where(
            np.cumsum(pca.explained_variance_ratio_) > local_variance_threshold
        )[0][0]
    vmin = np.percentile(local_dim, 5)
    vmax = np.percentile(local_dim, 95)

    return (points, local_dim)
