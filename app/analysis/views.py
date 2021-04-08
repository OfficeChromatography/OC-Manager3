from django.views.generic import FormView, View
from django.http import JsonResponse, HttpResponseBadRequest

from .core.hptlc_insight.hca_analysis import HCA_Analysis
from .forms import *
from .models import *
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import cv2
import numpy as np
import os
from django.core.files import File
from PIL import Image
from .core.hptlc_insight.track_detection import TrackDetection
from .core.hptlc_insight.track_inspection import TrackInspection
from .core.hptlc_insight.track_sort import TrackSort
from .core.hptlc_insight.pca_analysis import PCA_Analysis
from .core.hptlc_insight.heatmap import Heatmap

from django.core.files.base import ContentFile
from app.settings import MEDIA_ROOT
from django.forms.models import model_to_dict


def buffered_image_to_cv(buffered_image):
    image_as_np = np.frombuffer(buffered_image, dtype=np.uint8)
    img = cv2.imdecode(image_as_np, cv2.IMREAD_COLOR)
    return img


@method_decorator(csrf_exempt, name='dispatch')
class MethodList(View):

    def get(self, request):
        """Returns a list with all the Methods saved in DB"""
        method = Method_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = [[i.filename, i.id] for i in method]
        return JsonResponse(data_saved, safe=False)

    # def post(self, request):
    #     buffered_image = request.FILES['image'].file.read()  # IoBytes image
    #     image_as_np = np.frombuffer(buffered_image, dtype=np.uint8)
    #     img = cv2.imdecode(image_as_np, cv2.IMREAD_COLOR)
    #
    #     return JsonResponse({'works': "DSADSAD", })


@method_decorator(csrf_exempt, name='dispatch')
class TrackDetectionAPI(View):
    def dispatch(self, request, *args, **kwargs):
        if 'UPDATE' in request.POST:
            return self.update(request, *args, **kwargs)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, id):
        track_detection = TrackDetection_Db.objects.get(id=id)
        track_detection_object_dict = model_to_dict(track_detection)
        return JsonResponse({'data': track_detection_object_dict})

    def post(self, request, id):
        image = Images_Db.objects.get(id=id)
        image_path = image.image.path
        form = TrackDetectionForm(request.POST)
        if form.is_valid():
            track_detection_object = form.save()
            track_detection_object_dict = model_to_dict(track_detection_object)
            data = form.cleaned_data
            #####WorkAround needs to be change it###
            data.pop('image')
            data['img_path'] = '/app/analysis/test/test_image.png'
            #############################################
            track_detection = TrackDetection(**form.cleaned_data)
        else:
            print(form.errors)
        return JsonResponse({'data': track_detection_object_dict})


class ChromatogramPlot(View):

    def get(self, request, id):
        plot_object = PlotOnChromatograms_Db.objects.get(id=id)
        response = {**model_to_dict(plot_object)}
        response['image'] = response['image'].path
        return JsonResponse({'data': response})

    def post(self, request, id):
        track_detection_object_dict, track_detection_object = get_track_detection_dict(id)
        track_detection = TrackDetection(**track_detection_object_dict)
        plot_on_chromatograms_form = PlotOnChromatogramsForm(request.POST)

        if plot_on_chromatograms_form.is_valid():
            plot_object = plot_on_chromatograms_form.save(commit=False)
            plot_object.track_detection = track_detection_object
            tracks_on_chromatogram_buffer = track_detection.plot_tracks_on_chrom(
                **plot_on_chromatograms_form.cleaned_data)
            try:
                os.remove(MEDIA_ROOT + f'/images/plot_on_chromatograms/plot_on_chrom_{id}.png')
            finally:
                plot_object.image.save(f'plot_on_chrom_{id}.png',
                                       ContentFile(tracks_on_chromatogram_buffer.getvalue()),
                                       save=True)
                response = {**model_to_dict(plot_object, exclude=['image']),
                            'image': plot_object.image.url}
                return JsonResponse({'data': response})
        else:
            return JsonResponse({'ERROR': plot_on_chromatograms_form.errors})


class TrackInspectionAPI(View):

    def post(self, request, id, track):
        track_detection_object_dict, track_detection_object = get_track_detection_dict(id)
        track_detection = TrackDetection(**track_detection_object_dict)
        track_buf, rgb_buf = TrackInspection().show_densitogram_and_signal(track_detection, int(track))

        track_inspection_object = TrackInspection_Db()
        track_inspection_object.track_number = int(track)
        track_inspection_object.track_detection = track_detection_object
        try:
            os.remove(MEDIA_ROOT + f'/images/inspection/rgb_densitogram/{id}_rgb_densitogram_{track}.png')
            os.remove(MEDIA_ROOT + f'/images/inspection/track/{id}_track_number_{track}.png')
        finally:
            track_inspection_object.track_image.save(f'{id}_track_number_{track}.png',
                                                     ContentFile(track_buf.getvalue()),
                                                     save=False)

            track_inspection_object.rgb_densitogram.save(f'{id}_rgb_densitogram_{track}.png',
                                                         ContentFile(rgb_buf.getvalue()),
                                                         save=True)
            response = model_to_dict(track_inspection_object)

            response['track_image'] = response['track_image'].url
            response['rgb_densitogram'] = response['rgb_densitogram'].url
            return JsonResponse({'data': response})

    def get(self, request, id):
        track_inspection_object = TrackInspection_Db.objects.get(id=id)
        response = model_to_dict(track_inspection_object)
        response['track_image'] = response['track_image'].url
        response['rgb_densitogram'] = response['rgb_densitogram'].url
        return JsonResponse({'data': response})


class TrackSortAPI(View):

    def post(self, request, id):
        track_detection_object_dict, track_detection_object = get_track_detection_dict(id)
        track_detection = TrackDetection(**track_detection_object_dict)

        track_sort_form = TrackSortForm(request.POST)
        if track_sort_form.is_valid():
            track_sort = TrackSort(track_detection, **track_sort_form.cleaned_data)
            tracks_sorted_image = track_sort.sort_tracks_by_rf()
            track_sort_object = track_sort_form.save(commit=False)
            track_sort_object.track_detection = track_detection_object
            try:
                os.remove(
                    MEDIA_ROOT + f'/images/track_sort/{id}_sorted_tracks_rf_{track_sort_form.cleaned_data["rf"]}.png')
            finally:
                track_sort_object.sorted_image.save(f'{id}_sorted_tracks_rf_{track_sort_form.cleaned_data["rf"]}.png',
                                                    ContentFile(tracks_sorted_image.getvalue()),
                                                    save=True)

                response = model_to_dict(track_sort_object)
                response['sorted_image'] = response['sorted_image'].url
                return JsonResponse({'data': response})

    def get(self, request, id):
        track_sorted_object = TrackSort_Db.objects.get(id=id)
        response = model_to_dict(track_sorted_object)
        response['sorted_image'] = response['sorted_image'].url
        return JsonResponse({'data': response})


class PCAAnalysisAPI(View):

    def post(self, request, id):
        track_detection_object_dict, track_detection_object = get_track_detection_dict(id)
        track_detection = TrackDetection(**track_detection_object_dict)
        pca_form = PCAAnalysisForm(request.POST)
        if pca_form.is_valid():
            pca = PCA_Analysis(track_detection, **pca_form.cleaned_data)
            pca_object = pca_form.save(commit=False)
            pca_object.track_detection = track_detection_object
            refname = preprocess_reference_for_naming(pca_form.cleaned_data["reference"])
            try:
                os.remove(MEDIA_ROOT + f'/images/pca_analysis/explained_variance/{id}_explained_variance_{refname}.png')
                os.remove(MEDIA_ROOT + f'/images/pca_analysis/pca/{id}_pca_{refname}.png')
            finally:
                pca_object.explained_variance.save(f'{id}_explained_variance_{refname}.png',
                                                   ContentFile(pca.plot_explained_variance().getvalue()),
                                                   save=False)

                pca_object.pca.save(f'{id}_pca_{refname}.png',
                                    ContentFile(pca.plot_pca().getvalue()),
                                    save=True)

                response = model_to_dict(pca_object)
                response['explained_variance'] = response['explained_variance'].url
                response['pca'] = response['pca'].url
                return JsonResponse({'data': response})
        else:
            return JsonResponse({'error': pca_form.errors})

    def get(self, request, id):
        pca_object = PCAAnalysis_Db.objects.get(id=id)
        response = model_to_dict(pca_object)
        response['explained_variance'] = response['explained_variance'].url
        response['pca'] = response['pca'].url
        return JsonResponse({'data': response})


class HeatmapAPI(View):

    def post(self, request, id):
        track_detection_object_dict, track_detection_object = get_track_detection_dict(id)
        track_detection = TrackDetection(**track_detection_object_dict)
        heatmap_form = HeatmapForm(request.POST)
        if heatmap_form.is_valid():
            heatmap = Heatmap(track_detection, **heatmap_form.cleaned_data)
            heatmap_object = heatmap_form.save(commit=False)
            heatmap_object.track_detection = track_detection_object
            refname = preprocess_reference_for_naming(heatmap_form.cleaned_data["reference"])
            try:
                os.remove(MEDIA_ROOT + f'/images/heatmap/{id}_heatmap_{refname}.png')
            finally:
                heatmap_object.heatmap.save(f'{id}_heatmap_{refname}.png',
                                            ContentFile(heatmap.plot_heatmaps().getvalue()),
                                            save=True)
                response = model_to_dict(heatmap_object)
                response['heatmap'] = response['heatmap'].url
                return JsonResponse({'data': response})

    def get(self, request, id):
        heatmap_object = Heatmap_Db.objects.get(id=id)
        response = model_to_dict(heatmap_object)
        response['heatmap'] = response['heatmap'].url
        return JsonResponse({'data': response})


class HCAAnalysisAPI(View):

    def post(self, request, id):
        track_detection_object_dict, track_detection_object = get_track_detection_dict(id)
        track_detection = TrackDetection(**track_detection_object_dict)
        hca_form = HCAAnalysisForm(request.POST)
        if hca_form.is_valid():
            hca = HCA_Analysis(track_detection, **hca_form.cleaned_data)
            hca_object = hca_form.save(commit=False)
            hca_object.track_detection = track_detection_object
            refname = preprocess_reference_for_naming(hca_form.cleaned_data["reference"])
            try:
                os.remove(MEDIA_ROOT + f'/images/hca_analysis/tracks/{id}_tracks_{refname}.png')
                os.remove(MEDIA_ROOT + f'/images/hca_analysis/hca/{id}_hca_{refname}.png')
            finally:
                hca_buf, hca_tracks_buf = hca.plot_dendrogram()
                hca_object.hca_tracks.save(f'{id}_tracks_{refname}.png',
                                           ContentFile(hca_tracks_buf.getvalue()),
                                           save=True)
                hca_object.hca.save(f'{id}_hca_{refname}.png',
                                    ContentFile(hca_buf.getvalue()),
                                    save=True)

                response = model_to_dict(hca_object)
                response['hca_tracks'] = response['hca_tracks'].url
                response['hca'] = response['hca'].url
                return JsonResponse({'data': response})
        else:
            return JsonResponse({'data': hca_form.errors})

    def get(self, request, id):
        hca_object = HCAAnalysis_Db.objects.get(id=id)
        response = model_to_dict(hca_object)
        response['hca_tracks'] = response['hca_tracks'].url
        response['hca'] = response['hca'].url
        return JsonResponse({'data': response})


@method_decorator(csrf_exempt, name='dispatch')
class ImageAPI(View):
    def dispatch(self, request, *args, **kwargs):
        if request.method == 'POST':
            return self.post(request, *args, **kwargs)
        elif request.method == 'GET':
            if 'id' in kwargs:
                return self.get(request, *args, **kwargs)
            else:
                return self.get_list(request, *args, **kwargs)

    def post(self, request):
        form = ImageUploadForm(request.POST, request.FILES)

        if form.is_valid():
            image = form.save()
            response = self.__image_for_response(image)
            return JsonResponse({'data': response})
        else:
            print(form.errors)
            return JsonResponse({'error': form.errors, }, safe=False)

    def get(self, request, id):
        image = Images_Db.objects.get(id=id)
        response = self.__image_for_response(image)
        return JsonResponse({'data': response, }, safe=False)

    def get_list(self, request):
        images = Images_Db.objects.all()
        data_saved = [[i.filename, i.id, i.image.url] for i in images]
        return JsonResponse({'images': data_saved, }, safe=False)

    def __image_for_response(self, image):
        response = model_to_dict(image)
        response['image'] = response['image'].url
        return response

def buffer_to_image(buffer):
    return cv2.imdecode(np.frombuffer(buffer.getbuffer(), np.uint8), -1)


def database_image_to_opencv(image):
    pil_image = Image.open(image).convert('RGB')
    open_cv_image = np.array(pil_image)
    return open_cv_image


def get_track_detection_dict(id):
    track_detection_object = TrackDetection_Db.objects.get(id=id)
    track_detection_object_dict = model_to_dict(track_detection_object, exclude=['id', ])
    image = Images_Db.objects.get(id=track_detection_object_dict['image'])
    track_detection_object_dict['image'] = database_image_to_opencv(image.image)
    return track_detection_object_dict, track_detection_object


def preprocess_reference_for_naming(ref):
    return ref.replace(",", "")
