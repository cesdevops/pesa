from django.contrib import admin
from .models import GramPanchayat, Kosh, Kosh_User

# @admin.register(GramPanchayat)
# class GramPanchayatAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'gram_panchayat_name',
#         'gram_panchayat_code',
#         'panchayat_samiti',
#         'village_count',
#         'status'
#     ]
#     search_fields = [
#         'gram_panchayat_name',
#         'gram_panchayat_code',
#         'contact_person'
#     ]
#     list_filter = [
#         'status',
#         'gram_panchayat_type',
#         'panchayat_samiti'
#     ]
#     list_per_page = 20


# @admin.register(Kosh)
# class KoshAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'kosh_name',
#         'kosh_code',
#         'gramPanchayat',
#         'status'
#     ]
#     search_fields = [
#         'kosh_name',
#         'kosh_code',

#     ]
#     list_filter = [
#         'status',
#     ]
#     list_per_page = 20


# @admin.register(KoshUser)
# class KoshUserAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'name',
#         'username',
#         'mobile',
#         'email',
#         'kosh',
#         'status'
#     ]
#     search_fields = [
#         'name',
#         'username',
#         'mobile',
#         'email'
#     ]
#     list_filter = [
#         'status',
#         'kosh'
#     ]
#     list_per_page = 20


# @admin.register(KoshCommittee)
# class KoshCommitteeAdmin(admin.ModelAdmin):
#     list_display = [
#         'id',
#         'name',
#         'role',
#         'mobile',
#         'kosh',
#         'status'
#     ]
#     search_fields = [
#         'name',
#         'mobile',
#         'email'
#     ]
#     list_filter = [
#         'status',
#         'role'
#     ]
#     list_per_page = 20