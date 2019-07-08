"""cmdb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import HomeView

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'server/', include('servers.urls', namespace='server')),
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^accounts/', include('accounts.urls', namespace='accounts')),
    url(r'^networks/', include('network.urls', namespace='network')),
    # url(r'^auto/', include('auto.urls', namespace='auto')),
    url(r'^report/', include('report.urls', namespace='report')),
    url(r'^pool/', include('IPpool.urls', namespace='pool')),
    url(r'^storage/', include('storage.urls', namespace='storage')),
    url(r'^scheduler/', include('scheduler.urls', namespace='scheduler')),
    url(r'^ssh/', include("ssh.urls", namespace="ssh")),
    # url(r'^zabbix/', include("zabbix_Secondary.urls", namespace="zabbix")),
]
