from scripts.hptlc_insight.analysis_core import imgs_to_densitograms, get_tracks, _create_reference_list, create_combined_data
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import pandas as pd

### Heatmap

def plot_corr_matrix(signals, type, references):
    fig, ax = plt.subplots(figsize=(24, 16))
    corr = signals.corr()
    hm = sns.heatmap(corr, annot=True, ax=ax, cmap="coolwarm",fmt='.2f',
                 linewidths=.05, vmin=0, vmax=1)
    fig.subplots_adjust(top=0.93)
    for entry in references:
        ax.add_patch(Rectangle((0, entry), signals.shape[1], 1, fill=False, edgecolor="black", lw=3))
        ax.add_patch(Rectangle((entry, 0), 1, signals.shape[1], fill=False, edgecolor="black", lw=3))
    ax.set(title="Track Correlation of the Combined %s Dataset\n" % type, xlabel="\nTrack Number", ylabel="Track Number\n")
    fig.savefig("media/heatmap-%s.png" % str(type.lower()), transparent=True, bbox_inches="tight")
    fig.clf()

class Heatmap():
    def __init__(self, track_detection, reference):
        self.tracks = get_tracks(track_detection)
        self.reference = _create_reference_list(reference)
        # self.signals_r = imgs_to_densitograms(self.tracks, 0)
        # self.signals_g = imgs_to_densitograms(self.tracks, 1)
        # self.signals_b = imgs_to_densitograms(self.tracks, 2)
        self.combined = create_combined_data(self.tracks)
  
    def plot_heatmaps(self):
        cols = [*range(1, len(self.combined)+1)]
        # r = pd.DataFrame(data=self.signals_r).transpose()
        # r.columns = cols
        # g = pd.DataFrame(data=self.signals_g).transpose()
        # g.columns = cols
        # b = pd.DataFrame(data=self.signals_b).transpose()
        # b.columns = cols
        # plot_corr_matrix(r, "Red", self.reference)
        # plot_corr_matrix(g, "Green", self.reference)
        # plot_corr_matrix(b, "Blue", self.reference)
        combined = pd.DataFrame(data=self.combined).transpose()
        combined.columns = cols
        plot_corr_matrix(combined, "RGB", self.reference)

