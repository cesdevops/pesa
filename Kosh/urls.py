from django.urls import path
from . import views

urlpatterns = [

    # ---------------------------------Kosh Login Kosh Management Urls ------------------------------------
    path('kosh-dashboard/', views.Kosh_Dashboard, name='Kosh_Dashboard'),
    path('switch-kosh/<int:kosh_id>/', views.Switch_Kosh, name='Switch_Kosh'),
    path('Kosh-Manage-Kosh-Committee/', views.Kosh_Manage_Kosh_Committee, name='Kosh-Manage-Kosh-Committee'),

    # ---------------------------------Superuser Login - Kosh Management Urls ------------------------------------
    path('Kosh-Manage-Grampanchayat/',views.Kosh_Manage_Grampanchayat,name='Kosh-Manage-Grampanchayat'),
    path('Kosh-Management/<int:grampanchayat_id>/',views.Kosh_Management,name='Kosh-Management'),
    
    path('Kosh-Add/<int:grampanchayat_id>/', views.Kosh_Add, name='Kosh-Add'),
    path('Kosh-Edit/<int:grampanchayat_id>/<int:kosh_id>/', views.Kosh_Edit, name='Kosh-Edit'),
    path('Kosh-Population/<int:grampanchayat_id>/<int:kosh_id>/', views.Kosh_Population_Manage, name='Kosh-Population-Manage'),
    path('Kosh-Population/<int:grampanchayat_id>/<int:kosh_id>/<int:population_id>/', views.Kosh_Population_Manage, name='Kosh-Population-Manage'),
    path('Kosh-Total-Population/<int:grampanchayat_id>/<int:kosh_id>/', views.Kosh_Total_Population_Manage, name='Kosh-Total-Population-Manage'),
    path('Kosh-Total-Population/<int:grampanchayat_id>/<int:kosh_id>/<int:total_population_id>/', views.Kosh_Total_Population_Manage, name='Kosh-Total-Population-Manage'),
    path('Kosh-Bank-Detail/<int:grampanchayat_id>/<int:kosh_id>/', views.Kosh_Bank_Detail_Manage, name='Kosh-Bank-Detail-Manage'),
    path('Kosh-Bank-Detail/<int:grampanchayat_id>/<int:kosh_id>/<int:bank_detail_id>/', views.Kosh_Bank_Detail_Manage, name='Kosh-Bank-Detail-Manage'),
    
    path('Kosh-Users/', views.Kosh_Users, name='Kosh-Users'),
    path('Kosh-Users/<int:grampanchayat_id>/', views.Kosh_Users, name='Kosh-Users-With-GP'),
    path('Kosh-Add-User/<int:grampanchayat_id>/', views.Kosh_Add_User, name='Kosh-Add-User'),
    path('Kosh-Edit-User/<int:grampanchayat_id>/<int:kosh_user_id>/', views.Kosh_Edit_User, name='Kosh-Edit-User'),
    

    path( 'Kosh-fund-alloted-details/', views.Kosh_fund_alloted_details,name='Kosh-fund-alloted-details'),





    # path('Super_User_Kosh_Add_Grampanchayat/',views.Super_User_Kosh_Add_Grampanchayat, name='Super_User_Kosh_Add_Grampanchayat'),


]