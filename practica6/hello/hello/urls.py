"""hello URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.conf.urls import include, url

from restaurants.views import login_action, register_action, index, user_view

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^login/', login_action, name="login"),
    url(r'^register/', register_action, name="register"),
    url(r'^user/(?P<username>[-\w]+)$', user_view, name='user_view'),
    url(r'^restaurants/', include('restaurants.urls')),
]
