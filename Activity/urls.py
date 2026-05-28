from django.urls import path
from . import views

urlpatterns = [

    path('Activity-Work-Master/',views.Activity_Work_Master,name='Activity-Work-Master'),
    path('Activity-Add-Work-Master/',views.Activity_Add_Work_Master,name='Activity-Add-Work-Master'),
    path('activity/work-detail/<int:work_id>/', views.Activity_Work_Detail, name='Activity-Work-Detail'),

    # ---------------------------------10 Stage Activity Work Master Urls ------------------------------------
    path('Activity-Administrative-Sanction/<int:work_id>/',views.Activity_Administrative_Sanction,name='Activity-Administrative-Sanction'),
    path('Activity-Technical-Sanction/<int:work_id>/',views.Activity_Technical_Sanction,name='Activity-Technical-Sanction'),
    path('Activity-Quotation-Tender/<int:work_id>/',views.Activity_Quotation_Tender,name='Activity-Quotation-Tender'),
    path('Activity-Work-Order/<int:work_id>/',views.Activity_Work_Order,name='Activity-Work-Order'),
    path('Activity-Work-Start/<int:work_id>/',views.Activity_Work_Start,name='Activity-Work-Start'),
    path('Activity-Work-In-Progress/<int:work_id>/',views.Activity_Work_In_Progress,name='Activity-Work-In-Progress'),
    path('Activity-Work-Final/<int:work_id>/',views.Activity_Work_Final,name='Activity-Work-Final'),
    path('Activity-Payment_Process/<int:work_id>/',views.Payment_Process,name='Activity-Payment_Process'),



]   