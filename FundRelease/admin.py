from django.contrib import admin
from .models import Fund_Release, Kosh_Fund_Allocation, HeadAllocation

                      
@admin.register(Fund_Release)
class FundReleaseAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'release_name',
        'financial_year',
        'zilla_parishad',
        'installment',
        'release_order_no',
        'release_date',
        'total_amount',
        'fund_distributed',
        'created_at',
    )

    list_filter = (
        'financial_year',
        'fund_distributed',
        'installment',
        'created_at',
    )

    search_fields = (
        'release_name',
        'release_order_no',
        'remarks',
    )

    ordering = ('-created_at',)
