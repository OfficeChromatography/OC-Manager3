from django.shortcuts import render
from django.views import View
# Create your views here.

class Sample(View):

    def get(self, request):
        return render(request,'sample.html',)

    def post(self, request):
        return render(request,'sample.html',{})
