"""e-commerce-evaluation URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path
from django.urls import include
from api import views
from django.views.generic.base import TemplateView

urlpatterns = [
    path(r'', TemplateView.as_view(template_name='index.html')),
    path('admin/', admin.site.urls),
    path('api/login', views.login),
    path('api/register', views.register),
    path('api/logout', views.logout),
    path('api/verify', views.verify),
    path('api/reset', views.reset),
    path('api/analyze_comment', views.analyze_comment),
    path('api/analyze_url', views.analyze_url),
    path('api/analyze_brand', views.analyze_brand),
    path('api/contact',views.contact),
]
