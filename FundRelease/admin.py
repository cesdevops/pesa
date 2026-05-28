from django.contrib import admin
from .models import Fund_Release,Kosh_Fund_Allocation, HeadAllocation


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
        'created_at'
    )

    list_filter = (
        'status',
        'allocated_date',
        'created_at'
    )

    search_fields = (
        'kosh__name',
        'fund_release__id',
        'remark'
    )

    readonly_fields = (
        'created_at',
        'updated_at'
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
        'created_at'
    )

    list_filter = (
        'created_at',
    )

    search_fields = (
        'kosh_head__name',
    )

    readonly_fields = (
        'created_at',
        'updated_at'
    )

    ordering = ('-created_at',)