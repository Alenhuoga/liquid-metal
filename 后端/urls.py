"""后端 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path,include
from demo import views


urlpatterns = [
    path('',views.index),
    path('admin/', admin.site.urls),
    path('post/',views.model),
    path('train/',views.train_platform),
    path('train/test/',views.eva),
    path('train/test/get/',views.monitor),
    path('train/test/density/',views.train_density),
    path('get/',views.hanshu),
    path('backup/',views.backup),
    path('load/',views.model_load),
    path('camera/',views.detact),
    path('camera_off/',views.camara_off),
]
