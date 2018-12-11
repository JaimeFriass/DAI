
from django.conf.urls import url

from . import views

urlpatterns = [
  url(r'^$', views.index, name='index'),
  # User settings
  url(r'^login/', views.login_action, name='login'),
  url(r'^logout/', views.logout_action, name='logout'),
  url(r'^register/', views.register_action, name='register'),
  url(r'^settings/', views.settings, name='settings'),
  url(r'^user/(?P<username>[-\w]+)$', views.user_view, name='user_view'),

  # Restaurants
  url(r'^index/', views.index, name='index'),
  url(r'^search/', views.restaurants_view, name='restaurants_view'),
  url(r'^view/(?P<id>[-\w]+)$', views.restaurant_view, name='restaurant_view'),
  url(r'^edit/(?P<id>[-\w]+)$', views.restaurant_edit, name='restaurant_edit'),
]