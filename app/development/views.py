from django.shortcuts import render
from django.views.generic import FormView, View
from django.http import JsonResponse
from django.shortcuts import render
from .forms import *
from .models import *
from django.forms.models import model_to_dict
from connection.forms import OC_LAB
import json
from finecontrol.forms import ZeroPosition_Form
from finecontrol.models import ZeroPosition
from finecontrol.calculations.DevCalc import calculateDevelopment

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
        data_saved = [[development.filename, development.id] for development in developments]
        return JsonResponse(data_saved, safe=False)

class DevelopmentDetail(View):
    def get(self, request, id):
        """Loads an object specified by ID"""
        id_object = id
        development_conf = model_to_dict(Development_Db.objects.filter(pk=id_object).filter(auth_id=request.user)[0])
        plate_properties_conf = model_to_dict(
            PlateProperties_Dev_Db.objects.get(id=development_conf['plate_properties']))
        developmentBandSettings_conf = model_to_dict(
            BandSettings_Dev_Db.objects.get(id=development_conf['developmentBandSettings']))
        pressure_settings_conf = model_to_dict(
            PressureSettings_Dev_Db.objects.get(id=development_conf['pressure_settings']))
        zero_position_conf = model_to_dict(ZeroPosition.objects.get(id=development_conf['zero_position']))
        flowrate_entry = Flowrate_Db.objects.filter(development_in_db=development_conf['id']).values()
        flowrate_conf = {'flowrate': [entry for entry in flowrate_entry]}

        development_conf.update(plate_properties_conf)
        development_conf.update(developmentBandSettings_conf)
        development_conf.update(pressure_settings_conf)
        development_conf.update(zero_position_conf)
        development_conf.update(flowrate_conf)
        return JsonResponse(development_conf)

    def post(self, request):
        """Save and Update Data"""
        development_form = Development_Form(request.POST, request.user)

        objects_save = data_validations_and_save(
            plate_properties = PlateProperties_Form(request.POST),
            pressure_settings = PressureSettings_Form(request.POST),
            zero_position = ZeroPosition_Form(request.POST),
            developmentBandSettings_form = DevelopmentBandSettings_Form(request.POST),
        )

        flowrateSettings = request.POST.get('flowrate')
        flowrateSettings_data = json.loads(flowrateSettings)

        # If everything is OK then it checks the name and tries to save the Complete Sample App
        if development_form.is_valid():
            id = request.POST.get("selected-element-id")
            try:
                development_instance = Development_Db.objects.get(pk=id)
                Flowrate_Db.objects.filter(development_in_db=development_instance.id).delete()
            except:
                development_instance = development_form.save(commit=False)
                development_instance.auth = request.user

            development_instance.pressure_settings=objects_save['pressure_settings']
            development_instance.plate_properties = objects_save['plate_properties']
            development_instance.developmentBandSettings = objects_save['developmentBandSettings_form']
            development_instance.zero_position = objects_save['zero_position']
            development_instance.save()

            for flow_value in flowrateSettings_data:
                    flowrate_form = Flowrate_Form(flow_value)
                    if flowrate_form.is_valid():
                        flowrate_form = flowrate_form.save(commit=False)
                        flowrate_form.development_in_db = development_instance
                        flowrate_form.save()
                    else:
                        JsonResponse({'error': flowrate_form.errors})
            return JsonResponse({'message':'Data !!'})


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
