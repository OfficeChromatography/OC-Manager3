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
from django.conf.urls import include
from django.conf import settings
from django.conf.urls.static import static


from pages import views as pageviews
from connection import views as conn_view
from connection.views import Connection_test
from finecontrol import views as fine_view
# from users import views as usersview

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', pageviews.home_view, name='home'),
    # path('', conn_view.connection_view, name='home'),
    path('', Connection_test.as_view(), name='home'),
    path('connection/', Connection_test.as_view(), name='connection'),
    path('motorcontrol/', fine_view.motorcontrol_view, name='motorcontrol'),




    # path('register/', usersview.register_view, name='register'),
    # path('api/user/', include('users_api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
