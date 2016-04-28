from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^new/$', views.create_new_schedule, name='new_schedule'),
    url(r'^(?P<schedule_id>\d+)$', views.edit_schedule, name='edit_schedule'),
    url(r'^availability/$', views.instructor_availability, name='availability')
]
