from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ShootConfigurationForm, CameraControlsForm, UserControlsForm, AligmentConfigurationForm, LedsControlsForm
from connection.forms import OC_LAB
from app.settings import STATIC_ROOT, MEDIA_ROOT
from .models import Images_Db
from django.core.files import File
from django.core.files.storage import FileSystemStorage
import time
import subprocess
from types import SimpleNamespace
import cv2 as cv
import numpy as np
from  django.http import QueryDict

MOTION_MODEL = ((0, 'Translation'),
                    (1, 'Euclidean'),
                    (2, 'Affine'),
                    (3, 'Homography'))


INITIALS = {'brightness': 50,
            'contrast': 0,
            'saturation': 0,
            'red_balance': 1000,
            'blue_balance': 1000,
            'sharpness': 0,
            'color_effects': 0,
            'power_line_frequency':1,
            'horizontal_flip':0,
            'vertical_flip':0,
            'rotate':0,
            'color_effects_cbcr':32896,

            'resolution':'1280x720',
            'pixelformat':3,

            'auto_exposure':0,
            'exposure_dynamic_framerate':0,
            'auto_exposure_bias':12,
            'exposure_time_absolute':1000,
            'exposure_metering_mode':0,
            'white_balance_auto_preset':1,
            'image_stabilization':0,
            'iso_sensitivity_auto':1,
            'iso_sensitivity':0,
            'scene_mode':0
            }

# Create your views here.
form={}
class Capture_View(View):
    def get(self, request):
        # FILE LOADING
        if 'LOADFILE' in request.GET:
            filename = request.GET.get('filename')
            image = Images_Db.objects.filter(uploader=request.user,filename=filename)
            url = image[0].url
            response = {'url':image[0].url,
                        'filename':image[0].filename,
                        'meta':'none yet'}
            return JsonResponse(response)

        if 'LISTLOAD' in request.GET:
            images = Images_Db.objects.filter(uploader=request.user).order_by('-id')
            names = [i.filename for i in images]
            return JsonResponse(names, safe=False)

        else:
            form['FormatControlsForm'] = ShootConfigurationForm(initial=INITIALS)
            form['CameraControlsForm'] = CameraControlsForm(initial=INITIALS)
            form['UserControlsForm'] = UserControlsForm(initial=INITIALS)
            form['LedsControlsForm'] = LedsControlsForm()
            form['list_load'] = Images_Db.objects.filter(uploader=request.user).order_by('-id')

            data={'url':'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
            return render(
                            request,
                            "capture.html",
                            {**form, **data}
                            )

    def post(self, request):
        print(request.POST)
        # SAVE IMAGE
        if 'SAVE' in request.POST:
            filename = request.POST['filename'];

            if Images_Db.objects.filter(filename=filename,uploader=request.user):
                return JsonResponse({'danger':'Filename already exist, change it!'})

            image = Images_Db()
            image.filename = filename
            image.url = request.POST['url'];
            image.uploader = request.user
            image.save()
            return JsonResponse({'success':'File saved!'})

        if 'REMOVE' in request.POST:
            # print(request.POST)
            filename = request.POST.get('filename')
            try:
                file = Images_Db.objects.get(filename=filename,uploader=request.user)
                file.delete()
            except:
                return JsonResponse({'warning':'Something went wrong!'})
            return JsonResponse({'success':'File removed!'})

        else:
            form['FormatControlsForm'] = ShootConfigurationForm(request.POST or None)
            form['CameraControlsForm'] = CameraControlsForm(request.POST or None)
            form['UserControlsForm'] = UserControlsForm(request.POST or None)
            form['LedsControlsForm'] = LedsControlsForm(request.POST or None)

            data={'url':'https://bitsofco.de/content/images/2018/12/Screenshot-2018-12-16-at-21.06.29.png'}
            if form['CameraControlsForm'].is_valid():
                for key, value in form['CameraControlsForm'].cleaned_data.items():
                    # print(f'{key}={value}')
                    subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
            else:
                print(form['CameraControlsForm'].errors)


            if form['UserControlsForm'].is_valid():
                for key, value in form['UserControlsForm'].cleaned_data.items():
                    # print(f'{key}={value}')
                    subprocess.run([f'v4l2-ctl -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
            else:
                print('Error user Control')

            if form['LedsControlsForm'].is_valid():
                led365 = form['LedsControlsForm'].cleaned_data['uv365_power']
                led278 = form['LedsControlsForm'].cleaned_data['uv278_power']

                OC_LAB.send_now(f'M42 P5 S{led365}')
                OC_LAB.send_now(f'M42 P4 S{led278}')
                time.sleep(1)
            else:
                print('Error LEDs Control')

            if form['FormatControlsForm'].is_valid():
                conf = form['FormatControlsForm'].cleaned_data

                width = conf['resolution'][0]
                height = conf['resolution'][1]
                pixelformat = conf['pixelformat']

                conf.pop('resolution')

                # set resolution
                subprocess.run([f'v4l2-ctl --set-fmt-video=width={width}',f'height={height}'],stdout=subprocess.DEVNULL, shell=True)
                # set pixelformat
                subprocess.call(['v4l2-ctl','--set-fmt-video',f'pixelformat={pixelformat}'],stdout=subprocess.DEVNULL, shell=True)
                for key, value in conf.items():
                    try:
                        subprocess.run([f'v4l2-ctl -d /dev/video0 -c {key}={value}'],stdout=subprocess.DEVNULL, shell=True)
                    except KeyError:
                        print('Error trying to configure. Wrong Camera?')

                # Take picture
                pixelformat=pixelformat.lower()
                subprocess.call(['v4l2-ctl','--stream-mmap','--stream-count=1','--stream-skip=3','--stream-to='+'./'+STATIC_ROOT+'/best.'+pixelformat])

                # Turn off leds
                OC_LAB.send_now('M42 P17 S0')
                OC_LAB.send_now('M42 P23 S0')

                fs = FileSystemStorage()
                photo = '.'+STATIC_ROOT+'/best.'+pixelformat

                with open(photo, 'rb') as f:
                    new_name = fs.save('best.'+pixelformat, File(f))
                    print(fs.url(new_name))
                    data = {
                        'url':request.META['HTTP_ORIGIN']+fs.url(new_name),
                        'new_name':new_name,
                    }



            return JsonResponse(data)

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
        # print(request.POST)
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
