"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
# from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include

from pages import views as pages_views
from accounts import views as accounts_views
from connection.views import Connection_test
from finecontrol.views import MotorControl, PumpControl

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Connection_test.as_view(), name='connection'),
    path('connection/', Connection_test.as_view(), name='connection'),
    path('motorcontrol/',  MotorControl.as_view(), name='motorcontrol'),
    path('pumpcontrol/',  PumpControl.as_view(), name='pumpcontrol'),
    path('login/',  accounts_views.login_view, name='login'),
    path('logout/',  accounts_views.logout_view, name='logout'),
    path('register/',  accounts_views.register_view, name='register'),
    path('profile/',  accounts_views.profile_view, name='profile'),
    path('monitor/', include('monitor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT)
