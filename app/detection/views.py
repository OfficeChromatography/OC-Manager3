from django.views.generic import FormView, View
from django.shortcuts import render
from django.views import View
from django.http import JsonResponse, HttpResponseBadRequest
from connection.forms import OC_LAB
from app.settings import STATIC_ROOT, MEDIA_ROOT
from .models import *
from django.core.files import File
from django.core.files.storage import FileSystemStorage
from django.forms.models import model_to_dict
from .hdr import *
import cv2
import numpy as np
from  django.http import QueryDict
import json

from django.core.files import File

from .takeimage import *
from django.core.exceptions import ObjectDoesNotExist
import os

from finecontrol.forms import data_validations, data_validations_and_save

MOTION_MODEL = ((0, 'Translation'),
                    (1, 'Euclidean'),
                    (2, 'Affine'),
                    (3, 'Homography'))


class DetectionView(FormView):
    def get(self, request):
        """Manage the HTML view in Development"""
        form={}
        initial = basic_conf()
        form['FormatControlsForm'] = ShootConfigurationForm(initial=initial)
        form['CameraControlsForm'] = CameraControlsForm(initial=initial)
        form['UserControlsForm'] = UserControlsForm(initial=initial)
        form['LedsControlsForm'] = LedsControlsForm(initial=initial)
        image_info={'url': 'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
        return render(request, 'capture.html', {**form, **image_info})

class TakeImage(View):
    def post(self,request):
        photo_shoot = PhotoShootManager(request)
        photo_shoot.are_shoot_options_correct()
        photo_shoot.set_camera_configurations()
        photo_shoot.shoot()
        photo_shoot.photo_correction()
        photo_object = photo_shoot.save_photo_in_db()
        photo_info = {
            'url': request.META['HTTP_ORIGIN']+photo_object.image.url,
            'new_name': photo_object.image.url,
            'id': photo_object.id,
        }
        return JsonResponse(photo_info)

class DetectionDetail(View):
    def delete(self, request, id):
        Method_Db.objects.get(pk=id).delete()
        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        method = Method_Db.objects.get(id=id_object, auth=request.user)
        images = Images_Db.objects.filter(method=method)


        if not Method_Db.objects.get(id=id_object, auth=request.user) or images.count()==0:
            response.update({"filename":getattr(method,"filename")})
            response.update({"id":id_object})
        
        else:
            url_list=[]
            id_list=[]

            
            pos = images.count() - 1
            if (pos<0): pos=0 
            imageconf = images[pos]
            
            user_conf = model_to_dict(imageconf.user_conf,
                                    fields=[field.name for field in imageconf.user_conf._meta.fields])
            leds_conf = model_to_dict(imageconf.leds_conf,
                                    fields=[field.name for field in imageconf.leds_conf._meta.fields])
            camera_conf = model_to_dict(imageconf.camera_conf,
                                    fields=[field.name for field in imageconf.camera_conf._meta.fields])
            
            for image in images:
                url_list.append(image.image.url)
                id_list.append(image.id)

            response.update({**{
                        'url': url_list,
                        'filename': image.method.filename,
                        'id': id_object,
                        'id_list': id_list,
                        'user_conf': user_conf,
                        'leds_conf': leds_conf,
                        'camera_conf': camera_conf,
                        'note': imageconf.note,
                        }})
        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        
        id = request.POST.get("selected-element-id")
        image_id = request.POST.get("image_id")
        # if not id or not Images_Db.objects.filter(method=Method_Db.objects.get(pk=id)):
        #     detection_form = Detection_Form(request.POST)
        #     if detection_form.is_valid():
        #         detection_instance = detection_form.save(commit=False)
        #         detection_instance.auth = request.user
        method_form = Method_Form(request.POST)

        if not id:
            method = method_form.save(commit=False)
            method.auth = request.user
            method.save()
        else:
            method = Method_Db.objects.get(pk=id)
            method_form = Method_Form(request.POST, instance=method)
            method_form.save()
            if image_id:
                image_instance = Images_Db.objects.get(id=image_id)
                image_instance.method = method
                image_instance.note = request.POST.get("note")
                image_instance.save()

        return JsonResponse({'message':'Data !!'})

class GetConfig(View):
    def get(self, request, id):
        image = Images_Db.objects.get(pk=id)
        response = {}
        user_conf = model_to_dict(image.user_conf,
                                fields=[field.name for field in image.user_conf._meta.fields])
        leds_conf = model_to_dict(image.leds_conf,
                                fields=[field.name for field in image.leds_conf._meta.fields])
        camera_conf = model_to_dict(image.camera_conf,
                                fields=[field.name for field in image.camera_conf._meta.fields])
        response.update({**{
                        'user_conf': user_conf,
                        'leds_conf': leds_conf,
                        'camera_conf': camera_conf,
                        'note': image.note,
                        }})
        return JsonResponse(response)

class Hdr_View(View):
    def get(self, request):
        form = {
            'AligmentConfigurationForm': AligmentConfigurationForm(initial={
                    'number_of_iterations': 5000,
                    'warp_mode': 0,
            }),
        }
        return render(request, "hdr.html", form)

    def post(self, request):
        fs = FileSystemStorage()
        form = AligmentConfigurationForm(QueryDict(request.POST.getlist('AligmentConfigurationForm')[0]))
        ids = request.POST.getlist('id[]')
        if not form.is_valid():
            # Check the form values
            return HttpResponseBadRequest("Wrong Parameters")
        elif len(ids)<2:
            # Check theres at least 2 image
            return HttpResponseBadRequest("Select at least 2 Valid Pictures")
        else:
            try:
                img_list = [cv2.imread(Images_Db.objects.get(id=id).image.path) for id in ids]
            except ValueError:
                return HttpResponseBadRequest("Select valid Pictures")

            processed_hdr = HDR(  img_list,
                                form.cleaned_data.get('warp_mode'),
                                form.cleaned_data.get('number_of_iterations')).process_images()
            if processed_hdr is None:
                return HttpResponseBadRequest('There was an error processing HDR on images')
            else:
                with open(processed_hdr, 'rb') as f:
                    object = Hdr_Image()
                    object.image.save(os.path.basename(processed_hdr), File(f))
                    object.save()
                    f.close()
                    response = {
                        'url':request.META['HTTP_ORIGIN']+object.image.url,
                        'new_name':object.image.name,
                        'method': MOTION_MODEL[form.cleaned_data.get('warp_mode')][1]
                    }
                return JsonResponse(response)

class Detection_Homming(View):
    def post(self, request):
        if request.POST.get('setzero'):
            print(request.POST)
            zeros_values = list(request.POST['setzero'].split(","))
            zero_on_DB = Detection_ZeroPosition( uploader = request.user,
                                     zero_x = float(zeros_values[0]),
                                     zero_y = float(zeros_values[1]))
            zero_on_DB.save()
            OC_LAB.send(f'G92X0Y0')
            return JsonResponse({'message':'ok'})
    def get(self, request):
        if 'getzero' in request.GET:
            last_zero_position = Detection_ZeroPosition.objects.filter(uploader=request.user).order_by('-id')[0]
            OC_LAB.send(f'G0X{last_zero_position.zero_x}Y{last_zero_position.zero_y}\nG92X0Y0')
        return JsonResponse({'message':'ok'})