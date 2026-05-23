from django.urls import path
from . import views

urlpatterns = [

    path('kosh-dashboard/',views.Kosh_Dashboard,name='Kosh_Dashboard'),

]