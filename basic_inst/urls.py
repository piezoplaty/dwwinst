from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data_wind', views.dataWind, name='dataWind'),
    url(r'^data_boat', views.dataBoat, name='dataBoat'),
]
