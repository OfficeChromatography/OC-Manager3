from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ShootConfigurationForm, CameraControlsForm, UserControlsForm, AligmentConfigurationForm, LedsControlsForm
from connection.forms import OC_LAB
from app.settings import STATIC_ROOT, MEDIA_ROOT
from .models import Images_Db, Detection_ZeroPosition
from django.core.files import File
from django.core.files.storage import FileSystemStorage

import cv2 as cv
import numpy as np
from  django.http import QueryDict
import json

from django.core.files import File

from .takeimage import *
from django.core.exceptions import ObjectDoesNotExist
import os

MOTION_MODEL = ((0, 'Translation'),
                    (1, 'Euclidean'),
                    (2, 'Affine'),
                    (3, 'Homography'))


# Create your views here.
form={}
class Capture_View(View):
    def get(self, request):
        # FILE LOADING
        if 'LOADFILE' in request.GET:
            id = int(request.GET.get('id'))
            print(id)
            image = Images_Db.objects.get(pk=id)
            metadata = {}
            # me = get_metadata(image)
            # print(me)
            response = {**{'url':image.photo.url,
                        'filename':image.filename,
                        # 'meta':me,
                        'id': image.id}}
            return JsonResponse(response)

        if 'LISTLOAD' in request.GET:
            images = Images_Db.objects.filter(uploader=request.user).order_by('-id')
            names = [[i.filename,i.id] for i in images]
            return JsonResponse(names, safe=False)

        else:
            initial = basic_conf()
            form['FormatControlsForm'] = ShootConfigurationForm(initial=initial)
            form['CameraControlsForm'] = CameraControlsForm(initial=initial)
            form['UserControlsForm'] = UserControlsForm(initial=initial)
            form['LedsControlsForm'] = LedsControlsForm(initial=initial)
            form['list_load'] = Images_Db.objects.filter(uploader=request.user).order_by('-id')
            OC_LAB.send('G0Y183F3000')
            image_info={'url':'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
            return render(
                            request,
                            "capture.html",
                            {**form, **image_info}
                            )

    def post(self, request):
        print(request.POST)
        # SAVE IMAGE
        if 'SAVE' in request.POST:
            user_images = Images_Db.objects.filter(uploader=request.user)
            photo = user_images.get(id=request.POST['id'])
            photo.filename = request.POST['filename']
            photo.save()
            return JsonResponse({'success':'File saved!'})

        if 'REMOVE' in request.POST:
            try:
                file = Images_Db.objects.get(id=request.POST.get('id'),uploader=request.user)
                path = os.path.join('./', str(file.photo))
                if os.path.exists(path):
                    os.remove(path)
                    file.delete()
            except:
                return JsonResponse({'warning':'Something went wrong!'})
            return JsonResponse({'success':'File removed!'})

        else:
            photo_path = take_photo(request)
            photo_path = manipulate(photo_path)
            image = save_photo_db(photo_path,request.user)

            image_info = {
                'url':request.META['HTTP_ORIGIN']+image.photo.url,
                'new_name':image.photo.url,
                'id':image.id,
            }
            return JsonResponse(image_info)

class Hdr_View(View):
    def get(self,request):
        form = {
            'AligmentConfigurationForm':AligmentConfigurationForm(initial={
                    'number_of_iterations':5000,
                    'warp_mode':0,
            }),
        }
        return render(request,"hdr.html",form)

    def post(self, request):
        fs = FileSystemStorage()

        form = AligmentConfigurationForm(QueryDict(request.POST.getlist('AligmentConfigurationForm')[0]))
        urls = request.POST.getlist('url[]')

        if not form.is_valid() or not urls:
            print("Error")
            print(form.errors)
            return JsonResponse({'message':'No images selected'})
        else:
            paths = []
            print(form.cleaned_data)
            for url in urls:
                paths.append(fs.path(url[url.rfind('/')+1:]))
            img_list = [cv.imread(path) for path in paths]
            test_mertens(   img_list,
                            form.cleaned_data.get('warp_mode'),
                            form.cleaned_data.get('number_of_iterations'))


            fs_results = FileSystemStorage()
            with open(f'{MEDIA_ROOT}/hdr/results/fusion_mertens_aligned.jpeg', 'rb') as f:
                new_name = fs_results.save(f'hdr/results/fusion_mertens_aligned.jpeg', File(f))
                data = {
                    'url':request.META['HTTP_ORIGIN']+fs_results.url(new_name),
                    'new_name':new_name,
                    'method': MOTION_MODEL[form.cleaned_data.get('warp_mode')][1]
                }
                print(data)
                data=null
            return JsonResponse(data)

def test_mertens(images, warp_mode, iterations):
    """MOTION_MODELS = ((0, 'Translation'),
                        (1, 'Euclidean'),
                        (2, 'Affine'),
                        (3, 'Homography'))"""
    # Convert to grey scale
    grey_images = []
    for i in images:
        grey_images.append(cv.cvtColor(i,cv.COLOR_BGR2GRAY))

    # Find size of 1 of the images
    sz = grey_images[0].shape

    # Define 2x3 or 3x3 matrices and initialize the matrix to identity
    if warp_mode == cv.MOTION_HOMOGRAPHY :
        warp_matrix = np.eye(3, 3, dtype=np.float32)
    else :
        warp_matrix = np.eye(2, 3, dtype=np.float32)

    # Specify the threshold of the increment
    # in the correlation coefficient between two iterations
    termination_eps = 1e-10;
    criteria = (cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, iterations,  termination_eps)

	# Run the ECC algorithm. The results are stored in warp_matrix.
    aligned_images = []
    for i in range(1,len(images)):
        (cc, warp_matrix) = cv.findTransformECC(grey_images[0],grey_images[i],warp_matrix, warp_mode, criteria, grey_images[0], 5)

        if warp_mode == cv.MOTION_HOMOGRAPHY :
            aligned_images.append(cv.warpPerspective (images[i], warp_matrix, (sz[1],sz[0]), flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP))
        else:
            aligned_images.append(cv.warpAffine(images[i], warp_matrix, (sz[1],sz[0]), flags=cv.INTER_LINEAR + cv.WARP_INVERSE_MAP))
        cv.imwrite(f'{MEDIA_ROOT}/hdr/aligned/aligned_image{i}.jpeg', aligned_images[i-1])
        cv.imwrite(f'{MEDIA_ROOT}/hdr/aligned/aligned_image0.jpeg', images[0])

    img_fn=[]
    for i in range(0,len(images)):
        img_fn.append(f'aligned_image{i}.jpeg')
    img_list = [cv.imread(f'{MEDIA_ROOT}/hdr/aligned/'+fn) for fn in img_fn]

    # Exposure fusion using Mertens
    merge_mertens = cv.createMergeMertens()
    res_mertens = merge_mertens.process(img_list)
    res_mertens_8bit = np.clip(res_mertens*255, 0, 255).astype('uint8')
    cv.imwrite(f'{MEDIA_ROOT}/hdr/results/fusion_mertens_aligned.jpeg', res_mertens_8bit)

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