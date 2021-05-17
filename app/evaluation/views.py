from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict

from detection.models import Images_Db
from finecontrol.models import Method_Db
from sampleapp.models import SampleApplication_Db

# from .forms import *
# from .models import *



class EvaluationView(FormView):
    def get(self, request):
        """Manage the HTML view in Evaluation"""
        return render(request,'evaluation.html',{})

class EvaluationDetails(FormView):
    def get(self, request, id):
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

            for image in images:
                url_list.append(image.image.url)
                id_list.append(image.id)

            response.update({**{
                        'url': url_list,
                        'id_list': id_list,
                        }})
        return JsonResponse(response)

class EvaluationBandSetup(FormView):
    def get(self, request, id):
        response={}
        id_object = id
        method = Method_Db.objects.get(id=id_object, auth=request.user)

        if not Method_Db.objects.get(id=id_object, auth=request.user) or not SampleApplication_Db.objects.get(method=method):
            response.update({"filename":getattr(method,"filename")})
            response.update({"id":id_object})
        else:
            sample_config = SampleApplication_Db.objects.get(method=method)
            #response.update(model_to_dict(sample_config.pressure_settings.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.plate_properties.get(), exclude=["id",]))
            response.update(model_to_dict(sample_config.band_settings.get(), exclude=["id",]))
            #response.update(model_to_dict(sample_config.zero_properties.get(), exclude=["id",]))
            #response.update(model_to_dict(sample_config.movement_settings.get(), exclude=["id",]))
            #response.update(model_to_dict(method))

            #bands_components = BandsComponents_Db.objects.filter(sample_application=sample_config.id).values()
            #response.update({'bands_components': [entry for entry in bands_components]})

        return JsonResponse(response)

