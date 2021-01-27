from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from django.forms.models import model_to_dict
import json
from types import SimpleNamespace

from .forms import *
from .models import *

from connection.forms import OC_LAB
from finecontrol.calculations.sampleAppCalc import *

forms = {
    'SampleApplication_Form': SampleApplication_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'BandSettings_Form': BandSettings_Form(),
    'MovementSettings_Form': MovementSettings_Form(),
    'PressureSettings_Form':PressureSettings_Form(),
    'BandComponents_Form':BandsComponents_Form(),
    'ZeroPosition_Form': ZeroPosition_Form()
    }


class SampleView(FormView):
    def get(self, request):
        """Manage the HTML view in SampleApp"""
        return render(request,'sample.html',{})

class SampleList(FormView):

    def get(self, request):
        """Returns a list with all the SampleApplications save in DB"""
        sample_application = SampleApplication_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = [[i.filename,i.id] for i in sample_application]
        return JsonResponse(data_saved, safe=False)

class SampleDetails(View):

    def delete(self, request, id):
        SampleApplication_Db.objects.get(pk=id).delete()
        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        response = {}
        sample_config = SampleApplication_Db.objects.get(pk=id_object)

        response.update(model_to_dict(sample_config.pressure_settings.get(), exclude=["id",]))
        response.update(model_to_dict(sample_config.plate_properties.get(), exclude=["id",]))
        response.update(model_to_dict(sample_config.band_settings.get(), exclude=["id",]))
        response.update(model_to_dict(sample_config.zero_properties.get(), exclude=["id",]))
        response.update(model_to_dict(sample_config.movement_settings.get(), exclude=["id",]))
        response.update(model_to_dict(sample_config))

        bands_components = BandsComponents_Db.objects.filter(sample_application=id_object).values()
        response.update({'bands_components': [entry for entry in bands_components]})

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        print(request.POST)
        id = request.POST.get("selected-element-id")

        bands_components = request.POST.get('table')
        bands_components = json.loads(bands_components)

        if not id:
            sample_form = SampleApplication_Form(request.POST)
            if sample_form.is_valid():
                sample_instance = sample_form.save(commit=False)
                sample_instance.auth = request.user
                sample_instance.save()
                objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST),
                    pressure_settings=PressureSettings_Form(request.POST),
                    zero_position=ZeroPosition_Form(request.POST),
                    band_settings=BandSettings_Form(request.POST),
                    movement_settings=MovementSettings_Form(request.POST)
                )
                sample_instance.pressure_settings.add(objects_save["pressure_settings"])
                sample_instance.plate_properties.add(objects_save["plate_properties"])
                sample_instance.zero_properties.add(objects_save["zero_position"])
                sample_instance.band_settings.add(objects_save["band_settings"])
                sample_instance.movement_settings.add(objects_save["movement_settings"])

        else:
            sample_instance = SampleApplication_Db.objects.get(pk=id)
            sample_form = SampleApplication_Form(request.POST, instance=sample_instance)
            sample_form.save()
            data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST,
                                                            instance=sample_instance.plate_properties.get()),
                    pressure_settings=PressureSettings_Form(request.POST,
                                                            instance=sample_instance.pressure_settings.get()),
                    zero_position=ZeroPosition_Form(request.POST,
                                                            instance=sample_instance.zero_properties.get()),
                    band_settings=BandSettings_Form(request.POST,
                                                            instance=sample_instance.band_settings.get()),
                    movement_settings=MovementSettings_Form(request.POST, instance=sample_instance.movement_settings.get())
                )
            sample_instance.flowrates.all().delete()

        for band_component in bands_components:
            band_component_form = BandsComponents_Form(band_component)
            if band_component_form.is_valid():
                band_component_object = band_component_form.save()
                sample_instance.band_components.add(band_component_object)

        return JsonResponse({'message':'Data !!'})

    # def post(self, request):
    #     # Check the data receive and save it
    #     sample_application_form  =   SampleApplication_Form(request.POST, request.user)
    #     objects_save = data_validations(
    #         plate_properties    =   PlateProperties_Form(request.POST),
    #         band_settings       =   BandSettings_Form(request.POST),
    #         movement_settings   =   MovementSettings_Form(request.POST),
    #         pressure_settings   =   PressureSettings_Form(request.POST),
    #         zero_position       =   ZeroPosition_Form(request.POST)
    #     )
    #     print(request.POST)
    #     table_data = json.loads(request.POST.get('table'))
    #     print(table_data)
    #     # If everything is OK then it checks the name and tries to save the Complete Sample App
    #     if sample_application_form.is_valid():
    #         filename = sample_application_form.cleaned_data['filename']
    #         in_db=SampleApplication_Db.objects.filter(filename=filename).filter(auth_id=request.user)
    #         # Check if theres
    #         if len(in_db)>0:
    #             in_db[0].movement_settings = objects_save['movement_settings']
    #             in_db[0].pressure_settings = objects_save['pressure_settings']
    #             in_db[0].plate_properties = objects_save['plate_properties']
    #             in_db[0].band_settings = objects_save['band_settings']
    #             in_db[0].zero_position = objects_save['zero_position']
    #             in_db[0].save()
    #             BandsComponents_Db.objects.filter(sample_application=in_db[0]).delete()
    #             for i in table_data:
    #                 bands_components_form = BandsComponents_Form(i)
    #                 if bands_components_form.is_valid():
    #                     bands_components_instance = bands_components_form.save(commit=False)
    #                     bands_components_instance.sample_application = in_db[0]
    #                     bands_components_instance.save()
    #                 else:
    #                     JsonResponse({'error':bands_components_form.errors})
    #
    #             return JsonResponse({'message':'Data updated!!'})
    #         else:
    #             sample_application_instance = sample_application_form.save(commit=False)
    #             sample_application_instance.auth = request.user
    #             sample_application_instance.movement_settings = objects_save['movement_settings']
    #             sample_application_instance.pressure_settings = objects_save['pressure_settings']
    #             sample_application_instance.plate_properties = objects_save['plate_properties']
    #             sample_application_instance.band_settings = objects_save['band_settings']
    #             sample_application_instance.zero_position = objects_save['zero_position']
    #             new_sample_application = sample_application_instance.save()
    #
    #
    #             for i in table_data:
    #                 bands_components_form = BandsComponents_Form(i)
    #                 if bands_components_form.is_valid():
    #                     bands_components_instance=bands_components_form.save(commit=False)
    #                     bands_components_instance.sample_application = sample_application_instance
    #                     bands_components_instance.save()
    #                 else:
    #                     JsonResponse({'error':bands_components_form.errors})
    #
    #             return JsonResponse({'message':f'The File {filename} was saved!'})
    #     else:
    #         return JsonResponse({'error':'Please fill in the filename!'})



    # def get(self, request, id):
    #     id_object=id
    #     sample_application_conf=model_to_dict(SampleApplication_Db.objects.filter(pk=id_object).filter(auth_id=request.user)[0])
    #     plate_properties_conf=model_to_dict(PlateProperties_Db.objects.get(id=sample_application_conf['plate_properties']))
    #     band_settings_conf=model_to_dict(BandSettings_Db.objects.get(id=sample_application_conf['band_settings']))
    #     movement_settings_conf=model_to_dict(MovementSettings_Db.objects.get(id=sample_application_conf['movement_settings']))
    #     pressure_settings_conf=model_to_dict(PressureSettings_Db.objects.get(id=sample_application_conf['pressure_settings']))
    #     zero_position_conf=model_to_dict(ZeroPosition.objects.get(id=sample_application_conf['zero_position']))
    #     bands_components = BandsComponents_Db.objects.filter(sample_application=SampleApplication_Db.objects.filter(pk=id_object).filter(auth_id=request.user)[0])
    #
    #     bands=[]
    #     for i, band in enumerate(bands_components):
    #         bands.append(model_to_dict(band))
    #     bands = {'bands':bands}
    #     sample_application_conf.update(bands)
    #     sample_application_conf.update(plate_properties_conf)
    #     sample_application_conf.update(band_settings_conf)
    #     sample_application_conf.update(movement_settings_conf)
    #     sample_application_conf.update(pressure_settings_conf)
    #     sample_application_conf.update(zero_position_conf)
    #     print(f'Property id:{id_object} of sample app loaded!')
    #     return JsonResponse(sample_application_conf)

    # def post(self, request):
    #     # Check the data receive and save it
    #     sample_application_form  =   SampleApplication_Form(request.POST, request.user)
    #     objects_save = data_validations_and_save(
    #         plate_properties    =   PlateProperties_Form(request.POST),
    #         band_settings       =   BandSettings_Form(request.POST),
    #         movement_settings   =   MovementSettings_Form(request.POST),
    #         pressure_settings   =   PressureSettings_Form(request.POST),
    #         zero_position       =   ZeroPosition_Form(request.POST)
    #     )
    #     print(request.POST)
    #     table_data = json.loads(request.POST.get('table'))
    #     print(table_data)
    #     # If everything is OK then it checks the name and tries to save the Complete Sample App
    #     if sample_application_form.is_valid():
    #         filename = sample_application_form.cleaned_data['filename']
    #         in_db=SampleApplication_Db.objects.filter(file_name=filename).filter(auth_id=request.user)
    #         # Check if theres
    #         if len(in_db)>0:
    #             in_db[0].movement_settings = objects_save['movement_settings']
    #             in_db[0].pressure_settings = objects_save['pressure_settings']
    #             in_db[0].plate_properties = objects_save['plate_properties']
    #             in_db[0].band_settings = objects_save['band_settings']
    #             in_db[0].zero_position = objects_save['zero_position']
    #             in_db[0].save()
    #             BandsComponents_Db.objects.filter(sample_application=in_db[0]).delete()
    #             for i in table_data:
    #                 bands_components_form = BandsComponents_Form(i)
    #                 if bands_components_form.is_valid():
    #                     bands_components_instance = bands_components_form.save(commit=False)
    #                     bands_components_instance.sample_application = in_db[0]
    #                     bands_components_instance.save()
    #                 else:
    #                     JsonResponse({'error':bands_components_form.errors})
    #
    #             return JsonResponse({'message':'Data updated!!'})
    #         else:
    #             sample_application_instance = sample_application_form.save(commit=False)
    #             sample_application_instance.auth = request.user
    #             sample_application_instance.movement_settings = objects_save['movement_settings']
    #             sample_application_instance.pressure_settings = objects_save['pressure_settings']
    #             sample_application_instance.plate_properties = objects_save['plate_properties']
    #             sample_application_instance.band_settings = objects_save['band_settings']
    #             sample_application_instance.zero_position = objects_save['zero_position']
    #             new_sample_application = sample_application_instance.save()
    #
    #
    #             for i in table_data:
    #                 bands_components_form = BandsComponents_Form(i)
    #                 if bands_components_form.is_valid():
    #                     bands_components_instance=bands_components_form.save(commit=False)
    #                     bands_components_instance.sample_application = sample_application_instance
    #                     bands_components_instance.save()
    #                 else:
    #                     JsonResponse({'error':bands_components_form.errors})
    #
    #             return JsonResponse({'message':f'The File {filename} was saved!'})
    #     else:
    #         return JsonResponse({'error':'Please fill in the filename!'})

class SampleAppPlay(View):
    def post(self, request):
        # Play button
        if 'START' in request.POST:
            if OC_LAB.paused == True:
                OC_LAB.resume()
            else:
                # Run the form validations and return the clean data
                forms_data = data_validations(  plate_properties_form    =   PlateProperties_Form(request.POST),
                                                band_settings_form       =   BandSettings_Form(request.POST),
                                                movement_settings_form   =   MovementSettings_Form(request.POST),
                                                pressure_settings_form   =   PressureSettings_Form(request.POST),
                                                zero_position_form       =   ZeroPosition_Form(request.POST))


                # Add table data
                forms_data.update({'table':json.loads(request.POST.get('table'))})

                # With the data, gcode is generated
                gcode = calculate(forms_data)

                # Printrun
                OC_LAB.print_from_list(gcode)
                return JsonResponse({'error':'f.errors'})


class CalcVol(View):
    def post(self, request):
        forms_data = data_validations(  plate_properties_form    =   PlateProperties_Form(request.POST),
                                        band_settings_form       =   BandSettings_Form(request.POST),
                                        movement_settings_form   =   MovementSettings_Form(request.POST),
                                        pressure_settings_form   =   PressureSettings_Form(request.POST),
                                        zero_position_form       =   ZeroPosition_Form(request.POST))
        forms_data.update({'table':json.loads(request.POST.get('table'))})
        data = SimpleNamespace(**forms_data)
        results = returnDropEstimateVol(data)
        return JsonResponse({'results':results})

# AUX Functions

def data_validations(**kwargs):
    # Iterate each form and run validations
    forms_data = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            forms_data.update(form.cleaned_data)
        else:
            print(f'Error on {key_form}')
            return
    return forms_data


# returns a dictionary with all objects saved.
def data_validations_and_save(**kwargs):
    objects_saved = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            objects_saved[key_form] = form.save()
        else:
            return JsonResponse({'error':f'Check {key_form}'})
    return objects_saved
