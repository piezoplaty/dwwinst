from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^single_inst$', views.single_inst, name='single_inst'),
    url(r'^view_controllers$', views.view_controllers, name='view_controllers'),
    url(r'^data_wind', views.dataWind, name='dataWind'),
    url(r'^data_boat', views.dataBoat, name='dataBoat'),
    url(r'^data_all', views.dataAll, name='dataAll'),
    url(r'^download', views.downloadTelemetryHistory, name='downloadTelemetryHistory')
]
