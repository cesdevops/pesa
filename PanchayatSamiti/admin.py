from django.contrib import admin
from .models import (
    Panchayat_Samiti,
    Panchayat_Samiti_User,
)


@admin.register(Panchayat_Samiti)
class PanchayatSamitiAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'panchayat_samiti_name',
        'panchayat_samiti_code',
        'zilla_parishad',
        'taluka',
        'status',
    )
    search_fields = (
        'panchayat_samiti_name',
        'panchayat_samiti_code',
    )
    list_filter = ('status', 'zilla_parishad', 'taluka')


@admin.register(Panchayat_Samiti_User)
class PanchayatSamitiUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'username',
        'mobile',
        'email',
        'panchayat_samiti',
        'status',
    )
    search_fields = (
        'name',
        'username',
        'mobile',
        'email',
    )
    list_filter = ('status', 'panchayat_samiti')