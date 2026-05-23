from django.contrib import admin
from .models import (
    Zilla_Parishad,
    Zilla_Parishad_User,
)


@admin.register(Zilla_Parishad)
class ZillaParishadAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'zillaParishad_name',
        'district',
        'zillaParishad_code',
        'status',
    )
    search_fields = (
        'zillaParishad_name',
        'district',
        'zillaParishad_code',
    )
    list_filter = ('status',)


@admin.register(Zilla_Parishad_User)
class ZillaParishadUserAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name',
        'username',
        'mobile',
        'email',
        'zilla_parishad',
        'status',
    )
    search_fields = (
        'name',
        'username',
        'mobile',
        'email',
    )
    list_filter = ('status', 'zilla_parishad')