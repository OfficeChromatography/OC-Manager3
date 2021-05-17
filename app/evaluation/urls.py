from django.urls import path
from .views import *
from analysis.views import *
from finecontrol.views import MethodList

urlpatterns = [
    path('evaluation/', EvaluationView.as_view(), name='evaluation'),
    path('evaluation/list/', MethodList.as_view(), name='evaluationlist'),
    path('evaluation/load/<int:id>/', EvaluationDetails.as_view(), name='imageload'),
    # path('sample/save/', SampleDetails.as_view(), name='samplesave'),
    # path('sample/delete/<int:id>/', SampleDelete.as_view(), name='sampledelete'),
    path('evaluation/bandsetup/<int:id>/', EvaluationBandSetup.as_view(), name='bandsetup'),


    path('trackdetection/<int:id>/', TrackDetectionAPI.as_view(), name='trackdetection'),
    path('trackdetection/', TrackDetectionAPI.as_view(), name='trackdetectionlist'),
    path('chromatogram/<int:id>/', ChromatogramPlot.as_view(), name='chromatogram'),

    path('trackinspect/<int:id>/<int:track>/', TrackInspectionAPI.as_view(), name='trackinspect'),
    path('trackinspect/<int:id>/', TrackInspectionAPI.as_view(), name='trackinspect'),

    path('tracksort/<int:id>/', TrackSortAPI.as_view(), name='tracksort'),

    path('pcaanalysis/<int:id>/', PCAAnalysisAPI.as_view(), name='pca'),

    path('heatmap/<int:id>/', HeatmapAPI.as_view(), name='heatmap'),

    path('hcaanalysis/<int:id>/', HCAAnalysisAPI.as_view(), name='hca'),

    path('image/', ImageAPI.as_view(), name='image'),
    path('image/<int:id>/', ImageAPI.as_view(), name='image'),

]
