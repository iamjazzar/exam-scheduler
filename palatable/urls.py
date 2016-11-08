from django.conf.urls import patterns, include, url
from django.contrib import admin

from palatablesite import views

admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^$', views.Home.as_view(), name='home'),

    url(r'^schedule/', include('scheduler.urls', namespace='schedule')),
    url(r'^admin/', include(admin.site.urls)),
)
