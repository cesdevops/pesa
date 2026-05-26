from django.contrib import admin
from .models import (
    Financial_Year,
    Head_Percentage,
    Kosh_Head,
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



@admin.register(Kosh_Head)
class KoshHeadAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'status', 'created_at', 'updated_at')
    list_filter = ('status',)
    search_fields = ('name',)
    ordering = ('-created_at',)


@admin.register(Head_Percentage)
class HeadPercentageAdmin(admin.ModelAdmin):
    list_display = ('id', 'kosh_head', 'percentage', 'created_at', 'updated_at')
    search_fields = ('kosh_head__name',)
    ordering = ('-created_at',)