from django.shortcuts import render


# Create your views here.
def register_view(request, *args, **kwargs):
    return render(request, "register.html", {})
