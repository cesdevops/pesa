from django.urls import path
from . import views

urlpatterns = [

    path('panchayat-samiti-dashboard/',views.PanchayatSamiti_Dashboard,name='PanchayatSamiti_Dashboard'),

    # ---------------------------------Superuser Urls ------------------------------------
    path('PS-Manage-Panchayat-Samitis/',views.PS_Manage_Panchayat_Samitis,name='PS-Manage-Panchayat-Samitis'),
    path('PS-Manage-Users/',views.PS_Manage_Users,name='PS-Manage-Users'),



]




     