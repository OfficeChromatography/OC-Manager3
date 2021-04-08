from django.db import models
from django.contrib.auth import get_user_model

from detection.models import Images_Db


# Create your models here.
class Track_Db(models.Model):
    number = models.DecimalField(null=True, decimal_places=0, max_digits=6)

class TrackDetection_Db(models.Model):
    image = models.ForeignKey('Images_Db', on_delete=models.CASCADE)
    number_of_tracks = models.IntegerField(null=True)
    track_width = models.FloatField(null=True)
    bands_start = models.FloatField(null=True)
    front = models.FloatField(null=True)

class PlotOnChromatograms_Db(models.Model):
    track_detection = models.ForeignKey('TrackDetection_Db', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/plot_on_chromatograms')
    show_tracks = models.BooleanField(default=True)
    show_signal = models.BooleanField(default=True)
    show_crop = models.BooleanField(default=True)
    show_track_numbers = models.BooleanField(default=True)
    track_colour = models.CharField(max_length=20)
    signal_colour = models.CharField(max_length=20)


class TrackInspection_Db(models.Model):
    track_detection = models.ForeignKey('TrackDetection_Db', on_delete=models.CASCADE)
    track_number = models.IntegerField(null=True)
    track_image = models.ImageField(upload_to='images/inspection/track')
    rgb_densitogram = models.ImageField(upload_to='images/inspection/rgb_densitogram')


class TrackSort_Db(models.Model):
    track_detection = models.ForeignKey('TrackDetection_Db', on_delete=models.CASCADE)
    rf = models.FloatField(null=True)
    sorted_image = models.ImageField(upload_to='images/track_sort/')


class PCAAnalysis_Db(models.Model):
    track_detection = models.ForeignKey('TrackDetection_Db', on_delete=models.CASCADE)
    reference = models.CharField(max_length=20)
    explained_variance = models.ImageField(upload_to='images/pca_analysis/explained_variance/')
    pca = models.ImageField(upload_to='images/pca_analysis/pca/')

class Heatmap_Db(models.Model):
    track_detection = models.ForeignKey('TrackDetection_Db', on_delete=models.CASCADE)
    reference = models.CharField(max_length=20)
    heatmap = models.ImageField(upload_to='images/heatmap/')
#
class HCAAnalysis_Db(models.Model):
    track_detection = models.ForeignKey('TrackDetection_Db', on_delete=models.CASCADE)
    reference = models.CharField(max_length=20)
    hca_tracks = models.ImageField(upload_to='images/hca_analysis/tracks/')
    num_clusters = models.IntegerField(null=True)
    hca = models.ImageField(upload_to='images/hca_analysis/hca/')

    # def test_hca_analysis(track_detection):
    # reference = "1"
    # num_tracks = 20
    # hca = HCA_Analysis(track_detection, reference, num_tracks)
    # hca_buf, hca_tracks_buf = hca.plot_dendrogram()
    # hca_img = buffer_to_image(hca_buf)
    # hca_tracks_img = buffer_to_image(hca_tracks_buf)
    #
    # cv2.imwrite("hca_img.png", hca_img)
    # cv2.imwrite("hca_tracks_img.png", hca_tracks_img)
    # assert os.path.isfile('hca_img.png')
    # assert os.path.isfile('hca_tracks_img.png')
    #
    # os.remove('hca_img.png')
    # os.remove('hca_tracks_img.png')

class Images_Db(models.Model):
    id = models.AutoField(primary_key=True)
    image = models.ImageField(upload_to='images/', default='/default.jpeg')
    filename = models.CharField(max_length=100, null=True)
    uploader = models.ForeignKey(
        get_user_model(),
        null=True,
        on_delete=models.CASCADE,
        blank=True,
    )
    datetime = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    note = models.TextField(default="", null=True, blank=True)
