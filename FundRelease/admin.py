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


@admin.register(Kosh_Fund_Allocation)
class KoshFundAllocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'fund_release',
        'kosh',
        'allocated_amount',
        'released_amount',
        'balance_amount',
        'allocated_date',
        'status',
        'created_at',
    )

    list_filter = (
        'status',
        'allocated_date',
        'created_at',
    )

    search_fields = (
        'kosh__name',
        'remark',
    )

    ordering = ('-created_at',)


@admin.register(HeadAllocation)
class HeadAllocationAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'kosh_fund_allocation',
        'kosh_head',
        'allocated_amount',
        'utilize_amount',
        'remaining_amount',
        'created_at',
    )

    list_filter = (
        'created_at',
        'updated_at',
    )

    search_fields = (
        'kosh_head__name',
    )

    ordering = ('-created_at',)