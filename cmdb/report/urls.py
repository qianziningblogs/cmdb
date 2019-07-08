
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url

from .views import (
    export_csv,
    asset_export_machine,
    down_demo,
    FileView,
)
urlpatterns = [
    url(r'^export/(?P<model>\w+)/$', export_csv, name="export_csv"),
    url(r'^machine/$', asset_export_machine, name="machine"),
    url(r'^cpu/$', asset_export_machine, name="cpu"),
    url(r'^mem/$', asset_export_machine, name="mem"),
    url(r'^disk/$', asset_export_machine, name="disk"),
    url(r'^network/$', asset_export_machine   , name="network"),
    
    # 下载demo
    url(r'downdemo/(?P<demo>\w+)/$',down_demo, name="down_demo"),
    
    # 批量导入
    url(r'^media/upload/$', FileView.as_view(), name="upload"),

]
