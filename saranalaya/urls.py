"""
URL configuration for saranalaya project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import include, path
from .views import redirect_to_admin
from admin_app.sites import saranalaya_admin_site


urlpatterns = [
    path('stats/', include("admin_app.urls")),
    path('admin/', saranalaya_admin_site.urls),
    path("i18n/", include("django.conf.urls.i18n")),
    path('', redirect_to_admin),
]
