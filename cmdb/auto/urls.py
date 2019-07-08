
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from .views import (
    autoreport,
)
from .auto import (
    AutoCreate,
    AutoList,
    AutoDetailView,
    AutoUpdateView
)
urlpatterns = [
    url(r'^autoreport/(?P<uuid>[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3})/$', autoreport,name="autoreport"),
    url(r'^autoreport/(?P<uuid>[0-9a-z]{32})/$', autoreport,name="autoreport"),
    url(r'auto/list/$', AutoList.as_view(), name='auto_list'),
    url(r'auto/create/$', AutoCreate.as_view(), name='auto_create'),
    url(r'auto/detail/(?P<pk>[\d]+)/$', AutoDetailView.as_view(), name='auto_detail'),
    url(r'auto/update/(?P<pk>[\d]+)/$', AutoUpdateView.as_view(), name='auto_update')
]
