from django.contrib import admin
from .models import (
    Activity,
    Work_Master,
    Administrative_Sanction,
    Technical_Sanction,
    Quotation_Tender,
    Work_Order,
    Work_Start,
    Work_In_Progress,
    Work_Final,
    Payment_Process,
    Physically_Complete,
    Success_Story,
)


# ─────────────────────────────────────────────────────────────
# ACTIVITY ADMIN
# ─────────────────────────────────────────────────────────────
@admin.register(Activity)
class ActivityAdmin(admin.ModelAdmin):
    list_display = ['id', 'activity_name', 'kosh_head', 'status', 'created_at']
    list_filter = ['status', 'created_at', 'updated_at']
    search_fields = ['activity_name', 'kosh_head__name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('activity_name', 'kosh_head', 'status')
        }),
        ('System Fields', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ─────────────────────────────────────────────────────────────
# INLINE CLASSES FOR WORK MASTER
# ─────────────────────────────────────────────────────────────
class AdministrativeSanctionInline(admin.StackedInline):
    model = Administrative_Sanction
    extra = 0
    fieldsets = (
        ('Sanction Details', {
            'fields': ('sanction_number', 'department_name', 'sanction_date', 'proposal_date')
        }),
        ('Financial Details', {
            'fields': ('estimated_amount', 'approved_amount')
        }),
        ('Work Details', {
            'fields': ('work_location', 'objective', 'beneficiary_details')
        }),
        ('Resolution Details', {
            'fields': ('resolution_number', 'resolution_date')
        }),
        ('Status & Remarks', {
            'fields': ('status', 'remarks')
        }),
        ('Documents', {
            'fields': ('resolution_document', 'proposal_document', 'budget_estimate_document', 
                      'approval_letter_document', 'other_document')
        }),
    )


class TechnicalSanctionInline(admin.StackedInline):
    model = Technical_Sanction
    extra = 0
    fieldsets = (
        ('Sanction Details', {
            'fields': ('technical_sanction_number', 'sanction_date', 'technical_category')
        }),
        ('Financial Details', {
            'fields': ('estimated_amount', 'approved_amount')
        }),
        ('Technical Details', {
            'fields': ('technical_specification', 'work_scope', 'site_details', 
                      'measurement_details', 'material_details')
        }),
        ('Engineer Details', {
            'fields': ('engineer_name', 'engineer_designation', 'inspection_date')
        }),
        ('Status & Remarks', {
            'fields': ('status', 'approval_remark')
        }),
        ('Documents', {
            'fields': ('technical_estimate_document', 'site_inspection_document', 
                      'engineer_report_document', 'drawing_plan_document', 
                      'approval_letter_document', 'other_document')
        }),
    )


class QuotationTenderInline(admin.StackedInline):
    model = Quotation_Tender
    extra = 0
    fieldsets = (
        ('Process Details', {
            'fields': ('process_type', 'process_number', 'process_date')
        }),
        ('Work Details', {
            'fields': ('work_name', 'work_description')
        }),
        ('Financial Details', {
            'fields': ('estimated_amount', 'finalized_amount')
        }),
        ('Contractor/Vendor Details', {
            'fields': ('vendor_name', 'contractor_name', 'contractor_mobile', 'contractor_address')
        }),
        ('Analysis & Remarks', {
            'fields': ('comparative_analysis', 'selection_reason', 'remarks')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Documents', {
            'fields': ('quotation_form_document', 'comparative_statement_document', 
                      'contractor_agreement_document', 'tender_document', 'other_document')
        }),
    )


class WorkOrderInline(admin.StackedInline):
    model = Work_Order
    extra = 0
    fieldsets = (
        ('Order Details', {
            'fields': ('work_order_number', 'work_order_date', 'work_name', 'work_description')
        }),
        ('Contractor Details', {
            'fields': ('contractor_name', 'contractor_mobile', 'contractor_address')
        }),
        ('Timeline', {
            'fields': ('work_start_date', 'expected_completion_date', 'actual_completion_date')
        }),
        ('Financial Details', {
            'fields': ('estimated_amount', 'approved_amount')
        }),
        ('Instructions & Status', {
            'fields': ('execution_instructions', 'category', 'remarks', 'status')
        }),
        ('Documents', {
            'fields': ('signed_work_order_document', 'agreement_document', 'other_document')
        }),
    )


class WorkStartInline(admin.StackedInline):
    model = Work_Start
    extra = 0
    fieldsets = (
        ('Start Details', {
            'fields': ('start_date', 'actual_start_date', 'expected_end_date')
        }),
        ('Site & Personnel', {
            'fields': ('site_location', 'supervisor_name', 'contractor_name')
        }),
        ('Status', {
            'fields': ('initial_work_status', 'remarks', 'status')
        }),
        ('Documents', {
            'fields': ('site_photo_1', 'site_photo_2', 'site_photo_3', 
                      'commencement_certificate_document', 'supervisor_report_document', 'other_document')
        }),
    )


class WorkInProgressInline(admin.StackedInline):
    model = Work_In_Progress
    extra = 0
    fieldsets = (
        ('Progress Details', {
            'fields': ('progress_title', 'progress_date')
        }),
        ('Work Status', {
            'fields': ('completed_work_details', 'pending_work_details', 'current_site_status')
        }),
        ('Site Details', {
            'fields': ('site_inspection_details', 'labour_count', 'material_used_details')
        }),
        ('Planning', {
            'fields': ('delay_reason', 'next_work_plan', 'remarks')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Documents', {
            'fields': ('progress_photo_1', 'progress_photo_2', 'progress_photo_3',
                      'inspection_report_document', 'milestone_report_document', 'other_document')
        }),
    )


class WorkFinalInline(admin.StackedInline):
    model = Work_Final
    extra = 0
    fieldsets = (
        ('Completion Details', {
            'fields': ('completion_date', 'final_work_status', 'final_report')
        }),
        ('Status & Remarks', {
            'fields': ('completion_remarks', 'status')
        }),
        ('Documents', {
            'fields': ('final_photo_1', 'final_photo_2', 'final_photo_3',
                      'completion_certificate_document', 'measurement_book_document', 
                      'final_report_document', 'other_document')
        }),
    )


class PaymentProcessInline(admin.StackedInline):
    model = Payment_Process
    extra = 0
    fieldsets = (
        ('Payment Details', {
            'fields': ('payment_type', 'payment_date', 'payment_amount')
        }),
        ('Billing Details', {
            'fields': ('bill_number', 'invoice_number')
        }),
        ('Status & Remarks', {
            'fields': ('payment_remark', 'status')
        }),
        ('Documents', {
            'fields': ('bill_document', 'invoice_document', 'payment_receipt_document', 
                      'voucher_document', 'other_document')
        }),
    )


class PhysicallyCompleteInline(admin.StackedInline):
    model = Physically_Complete
    extra = 0
    fieldsets = (
        ('Inspection Details', {
            'fields': ('inspection_date', 'inspection_officer_name', 'inspection_remark')
        }),
        ('Completion Details', {
            'fields': ('physical_completion_date', 'verification_status')
        }),
        ('Status', {
            'fields': ('status',)
        }),
        ('Documents', {
            'fields': ('verification_photo_1', 'verification_photo_2', 'verification_photo_3',
                      'inspection_report_document', 'completion_certificate_document', 
                      'officer_verification_letter_document', 'other_document')
        }),
    )


class SuccessStoryInline(admin.StackedInline):
    model = Success_Story
    extra = 0
    fieldsets = (
        ('Story Details', {
            'fields': ('title', 'description', 'impact_details')
        }),
        ('Beneficiary Details', {
            'fields': ('beneficiary_details', 'before_work_details', 'after_work_details')
        }),
        ('Status & Remarks', {
            'fields': ('remarks', 'status')
        }),
        ('Documents', {
            'fields': ('before_photo_1', 'before_photo_2', 'before_photo_3',
                      'after_photo_1', 'after_photo_2', 'after_photo_3',
                      'impact_report_document', 'beneficiary_document', 
                      'media_coverage_document', 'other_document')
        }),
    )


# ─────────────────────────────────────────────────────────────
# WORK MASTER ADMIN
# ─────────────────────────────────────────────────────────────
@admin.register(Work_Master)
class WorkMasterAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_name', 'work_code', 'kosh_fund_allocation', 
                   'overall_status', 'is_fully_completed', 'created_at']
    list_filter = ['overall_status', 'is_fully_completed', 'created_at']
    search_fields = ['work_name', 'work_code', 'contractor_name', 'work_location']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']
    
    inlines = [
        AdministrativeSanctionInline,
        TechnicalSanctionInline,
        QuotationTenderInline,
        WorkOrderInline,
        WorkStartInline,
        WorkInProgressInline,
        WorkFinalInline,
        PaymentProcessInline,
        PhysicallyCompleteInline,
        SuccessStoryInline,
    ]
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('work_name', 'work_code', 'work_description', 'work_location')
        }),
        ('Financial Information', {
            'fields': ('kosh_fund_allocation', 'estimated_amount', 'approved_amount')
        }),
        ('Contractor Information', {
            'fields': ('contractor_name',)
        }),
        ('Overall Status', {
            'fields': ('overall_status', 'is_fully_completed', 'fully_completed_date')
        }),
        ('Stage Statuses', {
            'fields': (
                'administrative_sanction_status', 'technical_sanction_status', 
                'quotation_tender_status', 'work_order_status', 'work_start_status',
                'work_progress_status', 'work_final_status', 'payment_status',
                'physical_verification_status', 'success_story_status'
            ),
            'classes': ('collapse',)
        }),
        ('Stage Completion Flags', {
            'fields': (
                'administrative_sanction_completed', 'technical_sanction_completed',
                'quotation_tender_completed', 'contractor_finalized', 'work_order_completed',
                'work_start_completed', 'work_progress_completed', 'work_final_completed',
                'payment_completed', 'physically_completed', 'success_story_completed'
            ),
            'classes': ('collapse',)
        }),
        ('Stage Completion Dates', {
            'fields': (
                'administrative_sanction_completed_date', 'technical_sanction_completed_date',
                'quotation_tender_completed_date', 'contractor_finalized_date', 
                'work_order_completed_date', 'work_start_completed_date',
                'work_progress_completed_date', 'work_final_completed_date',
                'payment_completed_date', 'physically_completed_date',
                'success_story_completed_date'
            ),
            'classes': ('collapse',)
        }),
        ('Work Timeline', {
            'fields': ('work_start_date', 'work_order_number'),
            'classes': ('collapse',)
        }),
        ('System Fields', {
            'fields': ('created_by', 'updated_by', 'created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )


# ─────────────────────────────────────────────────────────────
# STANDALONE MODEL ADMINS
# ─────────────────────────────────────────────────────────────
@admin.register(Administrative_Sanction)
class AdministrativeSanctionAdmin(admin.ModelAdmin):
    list_display = ['id', 'sanction_number', 'work_master', 'approved_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['sanction_number', 'department_name', 'work_master__work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Technical_Sanction)
class TechnicalSanctionAdmin(admin.ModelAdmin):
    list_display = ['id', 'technical_sanction_number', 'work_master', 'technical_category', 
                   'approved_amount', 'status', 'created_at']
    list_filter = ['status', 'technical_category', 'created_at']
    search_fields = ['technical_sanction_number', 'engineer_name', 'work_master__work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Quotation_Tender)
class QuotationTenderAdmin(admin.ModelAdmin):
    list_display = ['id', 'process_type', 'process_number', 'work_name', 'finalized_amount', 
                   'contractor_name', 'status', 'created_at']
    list_filter = ['process_type', 'status', 'created_at']
    search_fields = ['process_number', 'vendor_name', 'contractor_name', 'work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Work_Order)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_order_number', 'work_name', 'contractor_name', 
                   'approved_amount', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['work_order_number', 'contractor_name', 'work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Work_Start)
class WorkStartAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_master', 'start_date', 'actual_start_date', 
                   'supervisor_name', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['work_master__work_name', 'supervisor_name', 'contractor_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Work_In_Progress)
class WorkInProgressAdmin(admin.ModelAdmin):
    list_display = ['id', 'progress_title', 'work_master', 'progress_date', 
                   'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['progress_title', 'work_master__work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Work_Final)
class WorkFinalAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_master', 'completion_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['work_master__work_name', 'final_report']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Payment_Process)
class PaymentProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_master', 'payment_type', 'payment_amount', 
                   'bill_number', 'status', 'created_at']
    list_filter = ['payment_type', 'status', 'created_at']
    search_fields = ['bill_number', 'invoice_number', 'work_master__work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Physically_Complete)
class PhysicallyCompleteAdmin(admin.ModelAdmin):
    list_display = ['id', 'work_master', 'inspection_date', 'inspection_officer_name', 
                   'physical_completion_date', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['work_master__work_name', 'inspection_officer_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


@admin.register(Success_Story)
class SuccessStoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'work_master', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['title', 'description', 'work_master__work_name']
    list_per_page = 25
    readonly_fields = ['created_at', 'updated_at']


# ─────────────────────────────────────────────────────────────
# ADMIN SITE CONFIGURATION
# ─────────────────────────────────────────────────────────────
admin.site.site_header = "Work Management System"
admin.site.site_title = "Work Management Admin"
admin.site.index_title = "Work Management Dashboard"