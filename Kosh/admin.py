from django.contrib import admin

from .models import (
    GramPanchayat,
    Kosh,
    Kosh_Cast_Category,
    Kosh_Population,
    Kosh_Total_Population,
    Kosh_User,
    Kosh_Committee,
    Kosh_Bank_Detail,
)


@admin.register(GramPanchayat)
class GramPanchayatAdmin(admin.ModelAdmin):
    list_display = (
        'gram_panchayat_name',
        'gram_panchayat_code',
        'status',
        'created_at',
    )
    search_fields = (
        'gram_panchayat_name',
        'gram_panchayat_code',
    )
    list_filter = ('status',)


@admin.register(Kosh)
class KoshAdmin(admin.ModelAdmin):
    list_display = (
        'kosh_name',
        'kosh_code',
        'is_primary',
        'status',
    )
    search_fields = (
        'kosh_name',
        'kosh_code',
    )
    list_filter = (
        'status',
        'is_primary',
    )


@admin.register(Kosh_Cast_Category)
class KoshCastCategoryAdmin(admin.ModelAdmin):
    list_display = (
        'category_name',
        'created_at',
    )
    search_fields = ('category_name',)


@admin.register(Kosh_Population)
class KoshPopulationAdmin(admin.ModelAdmin):
    list_display = (
        'cast_category',
        'financial_year',
        'population_count',
        'status',
    )
    list_filter = (
        'status',
        'financial_year',
    )


@admin.register(Kosh_Total_Population)
class KoshTotalPopulationAdmin(admin.ModelAdmin):
    list_display = (
        'kosh',
        'financial_year',
        'total_population',
        'tribal_population',
    )
    list_filter = ('financial_year',)


@admin.register(Kosh_User)
class KoshUserAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'mobile',
        'username',
        'get_kosh_names',
        'status',
        'is_retired',
    )

    search_fields = (
        'name',
        'mobile',
        'username',
        'email',
        'kosh__kosh_name',
    )

    list_filter = (
        'status',
        'is_retired',
        'kosh',
    )

    # Left Side -> Right Side ManyToMany UI
    filter_horizontal = ('kosh',)

    def get_kosh_names(self, obj):
        return ", ".join(
            obj.kosh.values_list('kosh_name', flat=True)
        )

    get_kosh_names.short_description = "Kosh Names"

@admin.register(Kosh_Committee)
class KoshCommitteeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'role',
        'mobile',
        'kosh_name',
        'status',
    )
    search_fields = (
        'name',
        'mobile',
        'email',
    )
    list_filter = (
        'role',
        'status',
    )


@admin.register(Kosh_Bank_Detail)
class KoshBankDetailAdmin(admin.ModelAdmin):
    list_display = (
        'bank_name',
        'branch_name',
        'account_holder_name',
        'account_number',
        'status',
        'current_balance',
    )
    search_fields = (
        'bank_name',
        'account_holder_name',
        'account_number',
        'ifsc_code',
    )