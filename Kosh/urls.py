from django.urls import path
from . import views

urlpatterns = [

    path('kosh-dashboard/',views.Kosh_Dashboard,name='Kosh_Dashboard'),
    path('Super_User_Kosh_Add_Grampanchayat/',views.Super_User_Kosh_Add_Grampanchayat, name='Super_User_Kosh_Add_Grampanchayat'),

]