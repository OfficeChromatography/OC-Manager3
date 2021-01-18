from django.shortcuts import render
from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
import json
from finecontrol.calculations.DevCalc import calculateDevelopment
from django.core import serializers

forms = {
    'Development_Form': Development_Form(),
    'PlateProperties_Form': PlateProperties_Form(),
    'DevelopmentBandSettings_Form': DevelopmentBandSettings_Form(),
    'PressureSettings_Form': PressureSettings_Form(),
    'ZeroPosition_Form': ZeroPosition_Form(),
    'Flowrate_Form': Flowrate_Form(),
}


class DevelopmentView(FormView):
    def get(self, request):
        """Manage the HTML view in Development"""
        return render(request, 'development.html', {})


class DevelopmentList(FormView):

    def get(self, request):
        """Returns a list with all the SampleApplications save in DB"""
        developments = Development_Db.objects.filter(auth_id=request.user).order_by('-id')
        data_saved = [[development.filename, development.pk] for development in developments]
        return JsonResponse(data_saved, safe=False)

class DevelopmentDetail(View):
    def delete(self, request, id):
        Development_Db.objects.get(pk=id).delete()

        return JsonResponse({})

    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        print(f"ID:{id_object}")
        response = {}
        dev_config = Development_Db.objects.get(pk=id_object)

        response.update(model_to_dict(dev_config.pressure_settings.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config.plate_properties.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config.band_settings.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config.zero_properties.get(), exclude=["id",]))
        response.update(model_to_dict(dev_config))

        flowrate_entry = Flowrate_Db.objects.filter(development=id_object).values('value')
        response.update({'flowrate': [entry for entry in flowrate_entry]})

        return JsonResponse(response)

    def post(self, request):
        """Save and Update Data"""
        id = request.POST.get("selected-element-id")
        print(request.POST)
        flowrate = request.POST.get('flowrate')
        flowrate = json.loads(flowrate)

        if not id:
            development_form = Development_Form(request.POST)
            if development_form.is_valid():
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user
                development_instance.save()
                objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST),
                    pressure_settings=PressureSettings_Form(request.POST),
                    zero_position=ZeroPosition_Form(request.POST),
                    band_settings=DevelopmentBandSettings_Form(request.POST),
                )
                development_instance.pressure_settings.add(objects_save["pressure_settings"])
                development_instance.plate_properties.add(objects_save["plate_properties"])
                development_instance.zero_properties.add(objects_save["zero_position"])
                development_instance.band_settings.add(objects_save["band_settings"])

                for flow_value in flowrate:
                    flowrate_form = Flowrate_Form(flow_value)
                    if flowrate_form.is_valid():
                        flowrate_object = flowrate_form.save()
                        development_instance.flowrates.add(flowrate_object)
        else:
            development_instance = Development_Db.objects.get(pk=id)
            development_form = Development_Form(request.POST, instance=development_instance)
            development_form.save()
            print(development_instance.pressure_settings.get())
            objects_save = data_validations_and_save(
                    plate_properties=PlateProperties_Form(request.POST,
                                                          instance=development_instance.plate_properties.get()),
                    pressure_settings=PressureSettings_Form(request.POST,
                                                            instance=development_instance.pressure_settings.get()),
                    # zero_position=ZeroPosition_Form(request.POST,
                    #                                 instance=development_instance.zero_properties.get()),
                    # band_settings=DevelopmentBandSettings_Form(request.POST,
                    #                                            instance=development_instance.band_settings.get()),
                )



        # if created:
        #     objects_save = data_validations_and_save(
        #         plate_properties=PlateProperties_Form(request.POST),
        #         pressure_settings=PressureSettings_Form(request.POST),
        #         zero_position=ZeroPosition_Form(request.POST),
        #         band_settings=DevelopmentBandSettings_Form(request.POST),
        #     )
        #
            # development_instance.pressure_settings.add(objects_save["pressure_settings"])
            # development_instance.plate_properties.add(objects_save["plate_properties"])
            # development_instance.zero_properties.add(objects_save["zero_position"])
            # development_instance.band_settings.add(objects_save["band_settings"])
        return JsonResponse({'message':'Data !!'})
        # else:


        # form = Development_Form(instance=development_instance, data=request.POST)
        # if form.is_valid():
        #     object=form.save()
        #     development_instance

        # development_form = Development_Form(development_instance, request.POST, request.user)


        #
        # Development_Db.objects.update_or_create(
        #     pk=id,
        #     flowrates=flowrate,
        #     plate_properties=objects_save['plate_properties'],
        #     pressure_settings=objects_save['pressure_settings'],
        #     zero_properties=objects_save['zero_position'],
        #     band_settings=objects_save['band_settings']
        # )


        # if development_form.is_valid():
        #     try:
        #         development_instance = Development_Db.objects.get(pk=id)
        #         # development_instance.flowrates.all().delete()
        #         # development_instance.pressure_settings.all().delete()
        #         # development_instance.plate_properties.all().delete()
        #         # development_instance.band_settings.all().delete()
        #         # development_instance.zero_properties.all().delete()
        #     except:
        #         development_instance = development_form.save(commit=False)
        #         development_instance.auth = request.user
        #         development_instance.save()


        # objects_save = data_validations_and_save(
        #     plate_properties=PlateProperties_Form(request.POST),
        #     pressure_settings=PressureSettings_Form(request.POST),
        #     zero_position=ZeroPosition_Form(request.POST),
        #     band_settings=DevelopmentBandSettings_Form(request.POST),
        # )
        #
        # print(development_instance)
        # development_instance.pressure_settings.add(objects_save["pressure_settings"])
        # development_instance.plate_properties.add(objects_save["plate_properties"])
        # development_instance.zero_properties.add(objects_save["zero_position"])
        # development_instance.band_settings.add(objects_save["band_settings"])
        #
        # for flow_value in flowrate:
        #     flowrate_form = Flowrate_Form(flow_value)
        #     if flowrate_form.is_valid():
        #         flowrate_object = flowrate_form.save()
        #         development_instance.flowrates.add(flowrate_object)
        #     else:
        #         JsonResponse({'error': flowrate_form.errors})



        # objects_save = data_validations_and_save(
        #     plate_properties=PlateProperties_Form(request.POST),
        #     pressure_settings=PressureSettings_Form(request.POST),
        #     zero_position=ZeroPosition_Form(request.POST),
        #     band_settings=DevelopmentBandSettings_Form(request.POST),
        # )
        #
        # flowrateSettings = request.POST.get('flowrate')
        # flowrateSettings_data = json.loads(flowrateSettings)
        #
        # # If everything is OK then it checks the name and tries to save the Complete Sample App
        # if development_form.is_valid():
        #     id = request.POST.get("selected-element-id")
        #     print(f"ID:{id}")
        #     try:
        #         development_instance = Development_Db.objects.get(pk=id)
        #         Flowrate_Db.objects.filter(development_in_db=development_instance.id).delete()
        #         print(f"En base de datos")
        #     except:
        #         development_instance = development_form.save(commit=False)
        #         development_instance.auth = request.user
        #         print(f"FUERA DE base de datos")
        #
        #     development_instance.filename = development_form.cleaned_data.get("filename")
        #     objects_save['pressure_settings']
        #     objects_save['plate_properties']
        #     objects_save['band_settings']
        #     objects_save['zero_position']
        #     development_instance.save()
        #
        #     for flow_value in flowrateSettings_data:
        #             flowrate_form = Flowrate_Form(flow_value)
        #             if flowrate_form.is_valid():
        #                 flowrate_form = flowrate_form.save(commit=False)
        #                 flowrate_form.development_in_db = development_instance
        #                 flowrate_form.save()
        #             else:
        #                 JsonResponse({'error': flowrate_form.errors})
        #     return JsonResponse({'message':'Data !!'})


class DevelopmentAppPlay(View):
        def post(self, request):
            if 'START' in request.POST:
                if OC_LAB.paused == True:
                    OC_LAB.resume()
                else:
                    # Run the form validations and return the clean data
                    forms_data = data_validations(plate_properties_form=PlateProperties_Form(request.POST),
                                                  pressure_settings_form=PressureSettings_Form(request.POST),
                                                  zero_position_form=ZeroPosition_Form(request.POST))

                    forms_data.update(json.loads(request.POST.get('devBandSettings')))
                    forms_data.update({'flowrate': json.loads(request.POST['flowrate'])})
                    # With the data, gcode is generated
                    gcode = calculateDevelopment(forms_data)

                    # Printrun
                    OC_LAB.print_from_list(gcode)
                    return JsonResponse({'error': 'f.errors'})


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


def data_validations_and_save(**kwargs):
    objects_saved = {}
    for key_form, form in kwargs.items():
        if form.is_valid():
            objects_saved[key_form] = form.save()
        else:
            print(form.errors)
            return JsonResponse({'error':f'Check {key_form}'})
    return objects_saved
