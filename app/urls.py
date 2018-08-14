from django.conf.urls import url
from .views import img_list,get_time
urlpatterns = [
    url(r'^app/$', img_list, name='img_list'),
    url(r'^gmtTime/$', get_time, name='get_time'),
]