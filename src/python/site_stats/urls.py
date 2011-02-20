from django.conf.urls.defaults import *

urlpatterns = patterns(
    'site_stats.views',
    url(r'^$', 'index'),
    url(r'^map/$', 'map'),
    )
