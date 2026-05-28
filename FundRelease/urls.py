from django.urls import path
from . import views



urlpatterns = [
    path('ZP-Fund-Release/', views.ZP_Fund_Release, name='ZP-Fund-Release'),
    path('ZP-Allocation-Chart/<str:financial_year>/<int:zp_id>/<int:fund_id>/', views.ZP_Allocation_Chart, name='ZP-Allocation-Chart'),
    path('ZP-Allocation-Chart/<str:financial_year>/<int:zp_id>/<int:fund_id>/allocate/', views.ZP_Kosh_Fund_Allocation, name='ZP-Kosh-Fund-Allocation'),  # ADD THIS
]

