from django.contrib import admin
from .models import Fund_Release


@admin.register(Fund_Release)
class FundReleaseAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'financial_year',
        'added_by',
        'release_name',
        'installment',
        'release_order_no',
        'release_date',
        'total_amount',
        'created_at',
    )

    search_fields = (
        'release_name',
        'release_order_no',
        'installment',
        'added_by__name',
        'added_by__username',
    )

    list_filter = (
        'financial_year',
        'installment',
        'release_date',
        'created_at',
    )

    ordering = ('-id',)