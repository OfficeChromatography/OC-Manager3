from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from .forms import ShootConfigurationForm
# Create your views here.
form={}
class Capture_View(View):
    def get(self, request):
        form['form'] = ShootConfigurationForm()
        print(form['form'])
        return render(
                        request,
                        "capture.html",
                        form
                        )

    def post(self, request):
        form['form'] = ShootConfigurationForm(request.POST or None)
        if form['form'].is_valid():
            form['form'].cleaned_data
            form['form'].TakeaPhoto()
        return render(
                        request,
                        "capture.html",
                        form
                        )
