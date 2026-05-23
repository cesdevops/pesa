from django.urls import path
from . import views

urlpatterns = [

    path('panchayat-samiti-dashboard/',views.PanchayatSamiti_Dashboard,name='PanchayatSamiti_Dashboard'),

    # ---------------------------------Superuser Urls ------------------------------------
    path('PS-Manage-Panchayat-Samitis/',views.PS_Manage_Panchayat_Samitis,name='PS-Manage-Panchayat-Samitis'),
    path('api/get-talukas-by-district/<int:district_id>/', views.get_talukas_by_district, name='get_talukas_by_district'),
    
    path('PS-Manage-Users/',views.PS_Manage_Users,name='PS-Manage-Users'),
    


    ]




     