from django.contrib import admin
from .models import (
    Financial_Year,
    Super_User,
    District,
    Taluka,
)


@admin.register(Financial_Year)
class FinancialYearAdmin(admin.ModelAdmin):
    list_display = ('id', 'year', 'start_date', 'end_date', 'status')
    search_fields = ('year',)
    list_filter = ('status',)


@admin.register(Super_User)
class SuperUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'username', 'mobile', 'email', 'status')
    search_fields = ('name', 'username', 'mobile', 'email')
    list_filter = ('status',)


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Taluka)
class TalukaAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'district')
    search_fields = ('name', 'district__name')
    list_filter = ('district',)