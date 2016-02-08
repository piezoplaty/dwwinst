from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^data_wind_speed', views.dataWindSpeed, name='dataWindSpeed'),
]
