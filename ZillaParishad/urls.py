from django.urls import path
from . import views

urlpatterns = [

    path('ZP-Dashboard/',views.ZP_Dashboard,name='ZP-Dashboard'),
    
    # -------------------------Superuser Urls ------------------------------------
    path('ZP-Manage-Zilla-Parishad/',views.ZP_Manage_Zilla_Parishad,name='ZP-Manage-Zilla-Parishad'),
    path('ZP-Manage-Zilla-Parishad-User/', views.ZP_Manage_Zilla_Parishad_User,name='ZP-Manage-Zilla-Parishad-User'),


]