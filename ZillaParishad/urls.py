from django.urls import path
from . import views

urlpatterns = [

    path('ZP-Dashboard/',views.ZP_Dashboard,name='ZP-Dashboard'),
    
    

    path('ZP-Manage-Zilla-Parishad/',views.ZP_Manage_Zilla_Parishad,name='ZP-Manage-Zilla-Parishad'),
    path('ZP-Manage-Zilla-Parishad-User/', views.ZP_Manage_Zilla_Parishad_User,name='ZP-Manage-Zilla-Parishad-User'),




    # -------------------------Superuser Urls ------------------------------------
    # path('Superuser-Manage-Zilla-Parishad/',views.Superuser_Manage_ZillaParishad,name='Superuser-Manage-Zilla-Parishad'),

]