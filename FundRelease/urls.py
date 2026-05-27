from django.urls import path
from . import views

urlpatterns = [

    path('ZP-Fund-Release/',views.ZP_Fund_Release,name='ZP-Fund-Release'),

]   