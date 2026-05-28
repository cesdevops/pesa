from django.urls import path
from . import views

urlpatterns = [

<<<<<<< HEAD
    # path('Activity-Work-Master/',views.Activity_Work_Master,name='Activity-Work-Master'),
=======
    path('Activity-Work-Master/',views.Activity_Work_Master,name='Activity-Work-Master'),
    path('Activity-Add-Work-Master/',views.Activity_Add_Work_Master,name='Activity-Add-Work-Master'),
    

    # ---------------------------------10 Stage Activity Work Master Urls ------------------------------------
    path('Activity-Administrative-Sanction/<int:work_id>/',views.Activity_Administrative_Sanction,name='Activity-Administrative-Sanction'),
    path('Activity-Technical-Sanction/<int:work_id>/',views.Activity_Technical_Sanction,name='Activity-Technical-Sanction'),
    path('Activity-Quotation-Tender/<int:work_id>/',views.Activity_Quotation_Tender,name='Activity-Quotation-Tender'),
    path('Activity-Work-Order/<int:work_id>/',views.Activity_Work_Order,name='Activity-Work-Order'),
    path('Activity-Work-Start/<int:work_id>/',views.Activity_Work_Start,name='Activity-Work-Start'),


>>>>>>> main

]   