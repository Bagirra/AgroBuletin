"""AgroBuletin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from catalog import views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('admin/', admin.site.urls),
    re_path(r'^prilojenie/$', views.prilojenie, name='prilojenie'),
    re_path(r'^vita_de_vie/$', views.vita_de_vie, name='vita_de_vie'),
    re_path(r'^prun/$', views.prun, name='prun'),
    re_path(r'^mar/$', views.mar, name='mar'),
    re_path(r'^piersic/$', views.piersic, name='piersic'),
    re_path(r'^cires/$', views.cires, name='cires'),
    re_path(r'^cereale/$', views.cereale, name='cereale'),
    re_path(r'^calculator', views.calculator, name='calculator'),
    re_path(r'^weather', views.weather, name='weather'),
    re_path(r'^culture/$', views.CultureListView.as_view(), name='culture'),
    re_path(r'^culture/(?P<pk>\d+)$', views.CultureDetailView.as_view(), name='culture-detail'),
    re_path(r'^culture-detail/(?P<pk>\d+)$', views.VozdeistvieDetailView.as_view(), name='vozdeistvie-detail'),
    #path('cities/', CityListView.as_view(), name='city-list'),
    #path('cities/<int:pk>/', CityDetailView.as_view(), name='city-detail'),
    path('cities/<int:city_id>/temperatures/<int:temperature_id>/', views.temperature_detail, name='temperature-detail'),
]
urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)