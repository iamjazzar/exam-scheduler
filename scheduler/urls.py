from django.conf.urls import patterns, url
from django.contrib import admin

from scheduler import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    # url(r'^$', views.Home.as_view(), name='home'),
    url(r'^$', views.Schedule.as_view(), name='schedule'),
)
