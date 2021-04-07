#
#     hptlc-insight: automated hptlc analysis and evaluation
#     Copyright (C) 2015-2019 CMCC Foundation
#
#     This program is free software: you can redistribute it and/or modify
#     it under the terms of the GNU General Public License as published by
#     the Free Software Foundation, either version 3 of the License, or
#     (at your option) any later version.
#
#     This program is distributed in the hope that it will be useful,
#     but WITHOUT ANY WARRANTY; without even the implied warranty of
#     MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#     GNU General Public License for more details.
#
#     You should have received a copy of the GNU General Public License
#     along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
import numpy as np
import io
from .analysis_core import _create_reference_list, get_tracks, imgs_to_densitograms, create_combined_data
import pandas as pd
from sklearn.decomposition import PCA
#from sklearn import preprocessing
import matplotlib.pyplot as plt


def create_cols(signal_l):
    r = ['r' + str(i) for i in range(1, signal_l)]
    g = ['g' + str(i) for i in range(1, signal_l)]
    b = ['b' + str(i) for i in range(1, signal_l)]
    cols = [*r, *g, *b]
    return cols


def create_data_frame(num_tracks, signal_l):
    signal_l += 1
    tracks = ['track' + str(i) for i in range(0, num_tracks)]
    cols = create_cols(int(signal_l/3+1))
    return pd.DataFrame(columns=cols, index=tracks)


def _create_pca_data(tracks):
    rgb_signals = create_combined_data(tracks)
    num_tracks = rgb_signals.shape[0]
    sig_l = rgb_signals.shape[1]
    f = create_data_frame(num_tracks, sig_l)
    for idx, track in enumerate(f.index):
        signals = rgb_signals[idx]
        f.loc[track, 'r1':'b'+str(int(sig_l/3))] = signals
    return f


def _do_pca(data):
    pca = PCA()
    pca.fit(data)
    pca_data = pca.transform(data)
    return (pca, pca_data)


def _calculate_perc_var(pca):
    return np.round(pca.explained_variance_ratio_ * 100, decimals=1)


def _create_labels(prefix, length):
    return [prefix + str(x) for x in range(1, length + 1)]


def _create_pca_df(df, pca_data):
    rows, cols = df.shape
    labels = _create_labels('PC', rows)
    cols = _create_labels(' ', rows)
    pca_df = pd.DataFrame(pca_data, index=cols, columns=labels)
    return pca_df


class PCA_Analysis():

    def __init__(self, track_detection, reference):
        self.tracks = get_tracks(track_detection)
        #self.data = imgs_to_densitograms(self.tracks)
        self.data = _create_pca_data(self.tracks)
        (pca, pca_d) = _do_pca(self.data)
        self.pca = pca
        self.pca_d = pca_d
        self.reference_tracks = _create_reference_list(reference)
        self.var = _calculate_perc_var(self.pca)

    # Plot scree plot
    def plot_explained_variance(self):
        explained_variance_buf = io.BytesIO()

        labels = _create_labels('', len(self.var))
        plt.bar(x=range(1, len(self.var) + 1), 
                height=self.var, 
                tick_label=labels,
                color='darkgrey',
                width=0.6)
        for idx, percentage in enumerate(self.var):
            if percentage >= 10.0:
                plt.annotate(str(percentage)+"%", (idx +0.5, self.var[idx]+0.3))
            else:
                plt.annotate(str(percentage)+"%", (idx +0.7, self.var[idx]+0.3))
        plt.ylabel('Percentage\n')
        plt.xlabel('\nPrincipal Components')
        plt.title('Explained Variance\n')
        plt.savefig(explained_variance_buf, transparent=True, bbox_inches="tight")
        explained_variance_buf.seek(0)
        plt.close()
        return explained_variance_buf

    # Plot PCA
    def plot_pca(self):
        pcaplot_buf = io.BytesIO()
        pca_df = _create_pca_df(self.data, self.pca_d)
        ref_df = pca_df.iloc[self.reference_tracks, :]
        per_var = _calculate_perc_var(self.pca)
        plt.scatter(pca_df.PC1, pca_df.PC2,color='darkgrey')
        plt.scatter(ref_df.PC1, ref_df.PC2,color='red')
        plt.title('Principal Component Comparison\n')
        plt.xlabel('\nPC1 - {0}%'.format(self.var[0]))
        plt.ylabel('PC2 - {0}%'.format(self.var[1]))
        for sample in pca_df.index:
            plt.annotate(sample,
                         (pca_df.PC1.loc[sample], pca_df.PC2.loc[sample]))
        plt.savefig(pcaplot_buf, transparent=True, bbox_inches="tight")
        pcaplot_buf.seek(0)
        plt.close()
        return pcaplot_buf
