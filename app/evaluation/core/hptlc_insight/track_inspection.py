#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt

def tracks_to_densitograms(td):
    chromatogram = td.img                                                                                                                                                                                                  
    tracks = td.tracks
    return [t.to_rgb_densitogram(chromatogram) for t in tracks]

def tracks_to_imgs(td):
    chromatogram = td.img
    tracks = td.tracks
    return [t.to_image(chromatogram) for t in tracks]

def plot_rgb_signal(densitogram):
    rgb = ['red', 'green', 'blue']
    for idx, s in enumerate(densitogram):
        plt.plot(s, color=rgb[idx])
        plt.xlim(left=0)
    plt.xlim(right=len(s))

"""
def eval_track_list(track_list, num_tracks):
    if len(track_list) == 0:
        return np.arange(0,num_tracks)
    try:
        parts = track_list.split(',')
        nums = [int(p) for p in parts]
        return list(filter(lambda x: x >= 0 and x < num_tracks, nums))
    except ValueError:
        print("track list is illegal!")
        return []
"""

class TrackInspection():    
            
    def show_densitogram_and_signal(td, inspection_track):
        densitograms = tracks_to_densitograms(td)
        track_imgs = tracks_to_imgs(td)
        plt.imshow(track_imgs[int(inspection_track)-1]), plt.show()
        plt.gca().set(title='Track ' + str(inspection_track), ylabel="Track Width\n[px]\n")
        plt.savefig('media/track-image.png', transparent=True, bbox_inches="tight")
        plt.close()

        plot_rgb_signal(densitograms[int(inspection_track)-1]),      
        plt.gca().set(xlabel="\nLocation on Track [px]", ylabel="Intensity\n")
        plt.savefig('media/rgb-densitogram.png', transparent=True, bbox_inches="tight")
        plt.close()