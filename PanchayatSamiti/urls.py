from django.urls import path
from . import views

urlpatterns = [
# ---------------------------------Panchat Samit Urls ------------------------------------
    path('PS-Dashboard/',views.PS_Dashboard,name='PS-Dashboard'),
# ── GramPanchayat list under this PS ──
    path(
        'ps/grampanchayat/',
        views.PS_GramPanchayat_List,
        name='PS-GramPanchayat-List'
    ),
 
    # ── Kosh list for a specific GramPanchayat ──
    path(
        'ps/grampanchayat/<int:gp_id>/kosh/',
        views.PS_Kosh_List,
        name='PS-Kosh-List'
    ),
 
    # ── Kosh detail (bank, population, committee) ──
    path(
        'ps/grampanchayat/<int:gp_id>/kosh/<int:kosh_id>/',
        views.PS_Kosh_Detail,
        name='PS-Kosh-Detail'
    ),
 
    # ── Kosh users for a GramPanchayat ──
    path(
        'ps/grampanchayat/<int:gp_id>/kosh-users/',
        views.PS_Kosh_Users,
        name='PS-Kosh-Users'
    ),
    # ---------------------------------Superuser Urls ------------------------------------
    path('PS-Manage-Panchayat-Samitis/',views.PS_Manage_Panchayat_Samitis,name='PS-Manage-Panchayat-Samitis'),
    path('api/get-talukas-by-zilla-parishad/<int:zilla_parishad_id>/', views.get_talukas_by_zilla_parishad, name='get_talukas_by_zilla_parishad'),
    
    path('PS-Manage-Users/',views.PS_Manage_Users,name='PS-Manage-Users'),
    






    ]




     