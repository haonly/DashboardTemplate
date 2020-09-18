from django.conf.urls import url
from django.urls import path
from django.views.generic import TemplateView

from . import views

app_name = 'demo'
urlpatterns = [
    #url('', views.index, name='index'),
    url(r'^upload/', views.upload, name='upload'),
    url('', views.index, name='index'),
]
