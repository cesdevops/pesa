from django.urls import path
from . import views

urlpatterns = [

    path('PS-Dashboard/',views.PS_Dashboard,name='PS-Dashboard'),

    # ---------------------------------Superuser Urls ------------------------------------
    path('PS-Manage-Panchayat-Samitis/',views.PS_Manage_Panchayat_Samitis,name='PS-Manage-Panchayat-Samitis'),
    path('api/get-talukas-by-zilla-parishad/<int:zilla_parishad_id>/', views.get_talukas_by_zilla_parishad, name='get_talukas_by_zilla_parishad'),
    
    path('PS-Manage-Users/',views.PS_Manage_Users,name='PS-Manage-Users'),
    


    ]




     