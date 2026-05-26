from django.urls import path
from . import views

urlpatterns = [

    path('', views.Login, name='Login'),
    path('logout/', views.Logout, name='Logout'),
    path('SuperUser-Login/', views.SuperUser_Login, name='SuperUser-Login'),
    path('Superuser-Logout/',views.Superuser_Logout,name='Superuser-Logout'),
    path('Superuser-Dashboard/',views.Superuser_Dashboard,name='Superuser-Dashboard'),

    path('Manage-District/',views.Manage_District,name='Manage-District'),
    path('Manage-Taluka/',views.Manage_Taluka,name='Manage-Taluka'),

]   