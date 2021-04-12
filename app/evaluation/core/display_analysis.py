#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import cv2, cv
from scripts.hptlc_insight.track_detection import TrackDetection
from scripts.hptlc_insight.track_sort import TrackSort
from scripts.hptlc_insight.pca_analysis import PCA_Analysis
from scripts.hptlc_insight.hca_analysis import HCA_Analysis
from scripts.hptlc_insight.heatmap import Heatmap
from scripts.hptlc_insight.track_inspection import TrackInspection

plt.rcParams.update({'figure.figsize':(19, 10), 'figure.dpi':100, 'font.size': 16})

class AnalysisDisplay():

    # run function for execution with command: 
    #   python manage.py runsript XXX --script-args XXX
    def run(*args):
        img_dimensions = [0,0,0]
        image, num_tracks, track_width, bands_start, front, rf_value, reference, track_list, show_tracks, show_track_numbers, show_signal, show_crop, track_colour, signal_colour, adjusting, extra = args
        # converts image from django memorystorage format to a rgb matrix
        image = cv2.imdecode(np.fromstring(image.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        try:
            rf_value = float(rf_value) /100
        except:
            rf_value
        # run Trackdetection, if track_list is provided, single tracks can be shown
        td = TrackDetection(img=image, number_of_tracks = num_tracks, track_width=track_width, bands_start=bands_start, front=front)
        if track_list != "" and rf_value != "":
            img_dimensions = td.plot_tracks_on_chrom(show_track_numbers=show_track_numbers, show_crop=show_crop, show_signal=show_signal, show_tracks=show_tracks, track_colour=track_colour, signal_colour=signal_colour)    
        if track_list != "":
            TrackInspection.show_densitogram_and_signal(td, str(track_list))
        if rf_value != "" and adjusting == False:
            ts = TrackSort(td, rf_value)
            ts.sort_tracks_by_rf(float(rf_value)) 
        if adjusting == False and extra == "":
            # PCA Analysis
            pca = PCA_Analysis(td, reference)
            pca.plot_explained_variance()
            pca.plot_pca()
            # Heatmap Representation of Single Channels
            heatmap = Heatmap(td, reference)
            heatmap.plot_heatmaps()
            # HCA Analysis
            hca = HCA_Analysis(td, reference, num_tracks)
            hca.plot_dendrogram()

        return img_dimensions