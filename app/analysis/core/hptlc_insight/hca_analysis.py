from .analysis_core import get_tracks, _create_reference_list, imgs_to_densitograms, create_combined_data, create_reference_dict
from .pca_analysis import _create_pca_data
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram
import matplotlib.pyplot as plt
import numpy as np
import io

def agglomerative_clustering(tracks, num_clusters):
    signals = np.array(create_combined_data(tracks)) # signals of each track summed up over all
    cluster = AgglomerativeClustering(n_clusters=None, affinity='euclidean', linkage='ward', distance_threshold=0)  
    cluster.fit_predict(signals)  
    return cluster

def plot_multiple_tracks(td, tracks, order, references):
    hca_tracks_buf = io.BytesIO()
    track_imgs = [t.to_image(td.img, False) for t in tracks]
    h, w, c = np.array(track_imgs[0]).shape
    fig = plt.figure(figsize=(20,8))

    for idx in range(1, len(tracks)+1):
        frame = order[idx-1] in references   
        fig.add_subplot(1, len(tracks)+1, idx, frame_on=frame)
        plt.imshow(track_imgs[order[idx-1]-1], extent=[0, w, 0, h])
        plt.axis('off')
    ax = plt.gca()
    ax.axes.xaxis.set_visible(False)
    plt.savefig(hca_tracks_buf, transparent=True, bbox_inches="tight")
    hca_tracks_buf.seek(0)
    plt.close()
    return hca_tracks_buf

# https://scikit-learn.org/stable/auto_examples/cluster/plot_agglomerative_dendrogram.html#sphx-glr-auto-examples-cluster-plot-agglomerative-dendrogram-py
def plot_dendrogram(model, **kwargs):
    # Create linkage matrix and then plot the dendrogram

    # create the counts of samples under each node
    counts = np.zeros(model.children_.shape[0])
    n_samples = len(model.labels_)
    for i, merge in enumerate(model.children_):
        current_count = 0
        for child_idx in merge:
            if child_idx < n_samples:
                current_count += 1  # leaf node
            else:
                current_count += counts[child_idx - n_samples]
        counts[i] = current_count

    linkage_matrix = np.column_stack([model.children_, model.distances_,
                                      counts]).astype(float)

    # Plot the corresponding dendrogram
    clustered_order = dendrogram(linkage_matrix, **kwargs)["ivl"]
    return clustered_order

class HCA_Analysis():
    
    def __init__(self, track_detection, reference, num_clusters=5):
        self._td = track_detection
        self.tracks = get_tracks(track_detection)
        self.tracks_to_plot = track_detection.tracks
        self.reference_tracks = _create_reference_list(reference)
        self.reference_dict = create_reference_dict(self.tracks, self.reference_tracks)
        self.num_clusters = int(num_clusters)

    def plot_dendrogram(self):
        hca_buf = io.BytesIO()
        model = agglomerative_clustering(self.tracks, self.num_clusters)
        labels = [*range(1, len(self.tracks)+1)]
        clustered_order = plot_dendrogram(model, truncate_mode='level', p=10, labels=labels, leaf_font_size=int(len(labels)*1.25), color_threshold=2)
        ax = plt.gca()
        xlabels = ax.get_xmajorticklabels()
        for label in xlabels:
            label.set_color(self.reference_dict[label.get_text()])
        plt.title("Hierarchical Clustering of Tracks\n")
        plt.ylabel("Euclidean Distance\n")
        plt.savefig(hca_buf, transparent=True, bbox_inches="tight")
        hca_buf.seek(0)
        plt.close()
        hca_tracks_buf =plot_multiple_tracks(self._td, self.tracks_to_plot, clustered_order, self.reference_tracks)
        return hca_buf, hca_tracks_buf

