from django.urls import path
from . import views

urlpatterns = [
    path('bts-test/init/', views.init, name='bts_test_init'),
    path('bts-test/redirect/', views.redirect, name='bts_test_redirect'),
    path('bts-test/logout/', views.logout, name='bts_test_logout'),
] 