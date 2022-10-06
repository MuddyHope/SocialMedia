from . import views
from django.urls import path


urlpatterns = [
    path('', views.index , name = 'index'),
    path('signup', views.signup, name = 'signup'),
    path('setting', views.settings, name = 'setting'),
    path('signin', views.signin, name ='signin'),
    path('logout', views.logout, name = 'logout'),
    path('upload', views.upload, name = 'upload'),
]