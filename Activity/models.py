from django.db import models
from Kosh.models import Kosh_User
from FundRelease.models import Kosh_Fund_Allocation
from Main.models import Kosh_Head

    
# ─────────────────────────────────────────────────────────────
# ACTIVITY
# ─────────────────────────────────────────────────────────────

class Activity(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    activity_name = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active', null=True, blank=True)
    kosh_head = models.ForeignKey(Kosh_Head, on_delete=models.SET_NULL, null=True, blank=True, related_name='activities')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Activity"
        verbose_name_plural = "0.Activities"

    def __str__(self):
        return self.activity_name or ''

# WORK MASTER
# ─────────────────────────────────────────────────────────────

class Work_Master(models.Model):
    WORK_STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    # activity = models.ForeignKey(Activity, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_masters')
    kosh_fund_allocation = models.ForeignKey(Kosh_Fund_Allocation, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_masters')

    # Basic Work Information
    work_name = models.CharField(max_length=255, null=True, blank=True)
    work_code = models.CharField(max_length=100, null=True, blank=True)
    work_description = models.TextField(null=True, blank=True)
    work_location = models.CharField(max_length=255, null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    overall_status = models.CharField(max_length=50, choices=WORK_STATUS_CHOICES, default='Pending', null=True, blank=True)

    # Stage 1 — Administrative Sanction
    administrative_sanction_completed = models.BooleanField(default=False, null=True, blank=True)
    administrative_sanction_completed_date = models.DateTimeField(null=True, blank=True)
    administrative_sanction_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Stage 2 — Technical Sanction
    technical_sanction_completed = models.BooleanField(default=False, null=True, blank=True)
    technical_sanction_completed_date = models.DateTimeField(null=True, blank=True)
    technical_sanction_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Stage 3 — Quotation / Tender
    quotation_tender_completed = models.BooleanField(default=False, null=True, blank=True)
    quotation_tender_completed_date = models.DateTimeField(null=True, blank=True)
    quotation_tender_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)
    contractor_finalized = models.BooleanField(default=False, null=True, blank=True)
    contractor_finalized_date = models.DateTimeField(null=True, blank=True)
    contractor_name = models.CharField(max_length=255, null=True, blank=True)

    # Stage 4 — Work Order
    work_order_completed = models.BooleanField(default=False, null=True, blank=True)
    work_order_completed_date = models.DateTimeField(null=True, blank=True)
    work_order_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)
    work_order_number = models.CharField(max_length=100, null=True, blank=True)

    # Stage 5 — Work Start
    work_start_date = models.DateField(null=True, blank=True)
    work_start_completed = models.BooleanField(default=False, null=True, blank=True)
    work_start_completed_date = models.DateTimeField(null=True, blank=True)
    work_start_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Stage 6 — Work In Progress
    work_progress_completed = models.BooleanField(default=False, null=True, blank=True)
    work_progress_completed_date = models.DateTimeField(null=True, blank=True)
    work_progress_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Stage 7 — Work Final
    work_final_completed = models.BooleanField(default=False, null=True, blank=True)
    work_final_completed_date = models.DateTimeField(null=True, blank=True)
    work_final_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Stage 8 — Payment Process
    payment_completed = models.BooleanField(default=False, null=True, blank=True)
    payment_completed_date = models.DateTimeField(null=True, blank=True)
    payment_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)
    total_payment_amount = models.DecimalField(max_digits=15, decimal_places=2, default=0, null=True, blank=True)

    # Stage 9 — Physically Complete
    physically_completed = models.BooleanField(default=False, null=True, blank=True)
    physically_completed_date = models.DateTimeField(null=True, blank=True)
    physical_verification_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Stage 10 — Success Story
    success_story_completed = models.BooleanField(default=False, null=True, blank=True)
    success_story_completed_date = models.DateTimeField(null=True, blank=True)
    success_story_status = models.CharField(max_length=100, default='Pending', null=True, blank=True)

    # Final Completion
    is_fully_completed = models.BooleanField(default=False, null=True, blank=True)
    fully_completed_date = models.DateTimeField(null=True, blank=True)

    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='created_work_masters', null=True, blank=True)
    updated_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='updated_work_masters', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Master"
        verbose_name_plural = "00.Work Masters"

    def __str__(self):
        return self.work_name or ''


# ─────────────────────────────────────────────────────────────
# STAGE 1 — ADMINISTRATIVE SANCTION
# ─────────────────────────────────────────────────────────────

class Administrative_Sanction(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='administrative_sanctions', null=True, blank=True)
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='administrative_sanctions', null=True, blank=True)
    sanction_number = models.CharField(max_length=100, null=True, blank=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    sanction_date = models.DateField(null=True, blank=True)
    proposal_date = models.DateField(null=True, blank=True)
    work_location = models.CharField(max_length=255, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)
    beneficiary_details = models.TextField(null=True, blank=True)
    resolution_number = models.CharField(max_length=100, null=True, blank=True)
    resolution_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    resolution_document = models.FileField(upload_to='administrative_sanction/resolution/', null=True, blank=True)
    proposal_document = models.FileField(upload_to='administrative_sanction/proposal/', null=True, blank=True)
    budget_estimate_document = models.FileField(upload_to='administrative_sanction/budget/', null=True, blank=True)
    approval_letter_document = models.FileField(upload_to='administrative_sanction/approval/', null=True, blank=True)
    other_document = models.FileField(upload_to='administrative_sanction/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='administrative_sanctions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    resolution_document = models.FileField(upload_to='administrative_sanction/resolution/', null=True, blank=True)
    proposal_document = models.FileField(upload_to='administrative_sanction/proposal/', null=True, blank=True)
    budget_estimate_document = models.FileField(upload_to='administrative_sanction/budget/', null=True, blank=True)
    approval_letter_document = models.FileField(upload_to='administrative_sanction/approval/', null=True, blank=True)
    other_document = models.FileField(upload_to='administrative_sanction/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='administrative_sanctions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Administrative Sanction"
        verbose_name_plural = "1.Administrative Sanctions"
        verbose_name_plural = "1.Administrative Sanctions"

    def __str__(self):
        return f"{self.sanction_number or ''} - {self.work_master}"


# ─────────────────────────────────────────────────────────────
# STAGE 2 — TECHNICAL SANCTION
# ─────────────────────────────────────────────────────────────
        return f"{self.sanction_number or ''} - {self.work_master}"


# ─────────────────────────────────────────────────────────────
# STAGE 2 — TECHNICAL SANCTION
# ─────────────────────────────────────────────────────────────

class Technical_Sanction(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    CATEGORY_CHOICES = (
        ('Education', 'Education'),
        ('Healthcare', 'Healthcare'),
        ('Infrastructure', 'Infrastructure'),
        ('Water Supply', 'Water Supply'),
        ('Road Development', 'Road Development'),
        ('Sanitation', 'Sanitation'),
        ('Other', 'Other'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='technical_sanctions', null=True, blank=True)
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='technical_sanctions', null=True, blank=True)
    technical_sanction_number = models.CharField(max_length=100, null=True, blank=True)
    sanction_date = models.DateField(null=True, blank=True)
    technical_category = models.CharField(max_length=100, choices=CATEGORY_CHOICES, null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    technical_specification = models.TextField(null=True, blank=True)
    work_scope = models.TextField(null=True, blank=True)
    site_details = models.TextField(null=True, blank=True)
    measurement_details = models.TextField(null=True, blank=True)
    material_details = models.TextField(null=True, blank=True)
    engineer_name = models.CharField(max_length=255, null=True, blank=True)
    engineer_designation = models.CharField(max_length=255, null=True, blank=True)
    inspection_date = models.DateField(null=True, blank=True)
    approval_remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    technical_estimate_document = models.FileField(upload_to='technical_sanction/estimate/', null=True, blank=True)
    site_inspection_document = models.FileField(upload_to='technical_sanction/inspection/', null=True, blank=True)
    engineer_report_document = models.FileField(upload_to='technical_sanction/engineer/', null=True, blank=True)
    drawing_plan_document = models.FileField(upload_to='technical_sanction/drawing/', null=True, blank=True)
    approval_letter_document = models.FileField(upload_to='technical_sanction/approval/', null=True, blank=True)
    other_document = models.FileField(upload_to='technical_sanction/other/', null=True, blank=True)
    # System Fields
    # Documents
    technical_estimate_document = models.FileField(upload_to='technical_sanction/estimate/', null=True, blank=True)
    site_inspection_document = models.FileField(upload_to='technical_sanction/inspection/', null=True, blank=True)
    engineer_report_document = models.FileField(upload_to='technical_sanction/engineer/', null=True, blank=True)
    drawing_plan_document = models.FileField(upload_to='technical_sanction/drawing/', null=True, blank=True)
    approval_letter_document = models.FileField(upload_to='technical_sanction/approval/', null=True, blank=True)
    other_document = models.FileField(upload_to='technical_sanction/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='technical_sanctions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)


    class Meta:
        ordering = ['-id']
        verbose_name = "Technical Sanction"
        verbose_name_plural = "2.Technical Sanctions"
        verbose_name_plural = "2.Technical Sanctions"

    def __str__(self):
        return f"{self.technical_sanction_number or ''} - {self.work_master}"


# ─────────────────────────────────────────────────────────────
# STAGE 3 — QUOTATION / B1 / TENDER
# ─────────────────────────────────────────────────────────────

class Quotation_Tender(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Quotation Process', 'Quotation Process'),
        ('B1 Process', 'B1 Process'),
        ('Tender Process', 'Tender Process'),
        ('Contractor Finalized', 'Contractor Finalized'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    PROCESS_TYPE_CHOICES = (
        ('Quotation', 'Quotation'),
        ('B1', 'B1'),
        ('Tender', 'Tender'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='quotation_tenders', null=True, blank=True)
    process_type = models.CharField(max_length=50, choices=PROCESS_TYPE_CHOICES, null=True, blank=True)
    process_number = models.CharField(max_length=100, null=True, blank=True)
    process_date = models.DateField(null=True, blank=True)
    work_name = models.CharField(max_length=255, null=True, blank=True)
    work_description = models.TextField(null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    finalized_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_mobile = models.CharField(max_length=20, null=True, blank=True)
    contractor_address = models.TextField(null=True, blank=True)
    comparative_analysis = models.TextField(null=True, blank=True)
    selection_reason = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    quotation_form_document = models.FileField(upload_to='quotation_tender/quotation/', null=True, blank=True)
    comparative_statement_document = models.FileField(upload_to='quotation_tender/comparative/', null=True, blank=True)
    contractor_agreement_document = models.FileField(upload_to='quotation_tender/agreement/', null=True, blank=True)
    tender_document = models.FileField(upload_to='quotation_tender/tender/', null=True, blank=True)
    other_document = models.FileField(upload_to='quotation_tender/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='quotation_tender_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Quotation / B1 / Tender"
        verbose_name_plural = "3.Quotation / B1 / Tenders"

    def __str__(self):
        return f"{self.process_type or ''} - {self.work_name or ''}"


# ─────────────────────────────────────────────────────────────
# STAGE 4 — WORK ORDER
# ─────────────────────────────────────────────────────────────
        return f"{self.technical_sanction_number or ''} - {self.work_master}"


# ─────────────────────────────────────────────────────────────
# STAGE 3 — QUOTATION / B1 / TENDER
# ─────────────────────────────────────────────────────────────

class Quotation_Tender(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Quotation Process', 'Quotation Process'),
        ('B1 Process', 'B1 Process'),
        ('Tender Process', 'Tender Process'),
        ('Contractor Finalized', 'Contractor Finalized'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    PROCESS_TYPE_CHOICES = (
        ('Quotation', 'Quotation'),
        ('B1', 'B1'),
        ('Tender', 'Tender'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='quotation_tenders', null=True, blank=True)
    process_type = models.CharField(max_length=50, choices=PROCESS_TYPE_CHOICES, null=True, blank=True)
    process_number = models.CharField(max_length=100, null=True, blank=True)
    process_date = models.DateField(null=True, blank=True)
    work_name = models.CharField(max_length=255, null=True, blank=True)
    work_description = models.TextField(null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    finalized_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    vendor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_mobile = models.CharField(max_length=20, null=True, blank=True)
    contractor_address = models.TextField(null=True, blank=True)
    comparative_analysis = models.TextField(null=True, blank=True)
    selection_reason = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    quotation_form_document = models.FileField(upload_to='quotation_tender/quotation/', null=True, blank=True)
    comparative_statement_document = models.FileField(upload_to='quotation_tender/comparative/', null=True, blank=True)
    contractor_agreement_document = models.FileField(upload_to='quotation_tender/agreement/', null=True, blank=True)
    tender_document = models.FileField(upload_to='quotation_tender/tender/', null=True, blank=True)
    other_document = models.FileField(upload_to='quotation_tender/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='quotation_tender_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Quotation / B1 / Tender"
        verbose_name_plural = "3.Quotation / B1 / Tenders"

    def __str__(self):
        return f"{self.process_type or ''} - {self.work_name or ''}"


# ─────────────────────────────────────────────────────────────
# STAGE 4 — WORK ORDER
# ─────────────────────────────────────────────────────────────

class Work_Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_orders', null=True, blank=True)
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_orders', null=True, blank=True)
    work_order_number = models.CharField(max_length=100, null=True, blank=True)
    work_name = models.CharField(max_length=255, null=True, blank=True)
    work_description = models.TextField(null=True, blank=True)
    contractor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_mobile = models.CharField(max_length=20, null=True, blank=True)
    contractor_address = models.TextField(null=True, blank=True)
    work_order_date = models.DateField(null=True, blank=True)
    work_start_date = models.DateField(null=True, blank=True)
    expected_completion_date = models.DateField(null=True, blank=True)
    actual_completion_date = models.DateField(null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    execution_instructions = models.TextField(null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    approved_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    execution_instructions = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    signed_work_order_document = models.FileField(upload_to='work_order/signed/', null=True, blank=True)
    agreement_document = models.FileField(upload_to='work_order/agreement/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_order/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='created_work_orders', null=True, blank=True)
    updated_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='updated_work_orders', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    signed_work_order_document = models.FileField(upload_to='work_order/signed/', null=True, blank=True)
    agreement_document = models.FileField(upload_to='work_order/agreement/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_order/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='created_work_orders', null=True, blank=True)
    updated_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='updated_work_orders', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Order"
        verbose_name_plural = "4.Work Orders"
        verbose_name_plural = "4.Work Orders"

    def __str__(self):
        return f"{self.work_order_number or ''} - {self.work_name or ''}"


# ─────────────────────────────────────────────────────────────
# STAGE 5 — WORK START
# ─────────────────────────────────────────────────────────────
        return f"{self.work_order_number or ''} - {self.work_name or ''}"


# ─────────────────────────────────────────────────────────────
# STAGE 5 — WORK START
# ─────────────────────────────────────────────────────────────

class Work_Start(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Started', 'Started'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_starts', null=True, blank=True)
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_starts', null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    site_location = models.CharField(max_length=255, null=True, blank=True)
    supervisor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_name = models.CharField(max_length=255, null=True, blank=True)
    initial_work_status = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    site_photo_1 = models.ImageField(upload_to='work_start/photos/', null=True, blank=True)
    site_photo_2 = models.ImageField(upload_to='work_start/photos/', null=True, blank=True)
    site_photo_3 = models.ImageField(upload_to='work_start/photos/', null=True, blank=True)
    commencement_certificate_document = models.FileField(upload_to='work_start/certificate/', null=True, blank=True)
    supervisor_report_document = models.FileField(upload_to='work_start/supervisor/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_start/other/', null=True, blank=True)
    # System Fields
    started_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='started_works', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    site_photo_1 = models.ImageField(upload_to='work_start/photos/', null=True, blank=True)
    site_photo_2 = models.ImageField(upload_to='work_start/photos/', null=True, blank=True)
    site_photo_3 = models.ImageField(upload_to='work_start/photos/', null=True, blank=True)
    commencement_certificate_document = models.FileField(upload_to='work_start/certificate/', null=True, blank=True)
    supervisor_report_document = models.FileField(upload_to='work_start/supervisor/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_start/other/', null=True, blank=True)
    # System Fields
    started_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='started_works', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Start"
        verbose_name_plural = "5.Work Starts"
        verbose_name_plural = "5.Work Starts"

    def __str__(self):
        return f"{self.work_master} - {self.status}"

        return f"{self.work_master} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 6 — WORK IN PROGRESS
# ─────────────────────────────────────────────────────────────

# ─────────────────────────────────────────────────────────────
# STAGE 6 — WORK IN PROGRESS
# ─────────────────────────────────────────────────────────────

class Work_In_Progress(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Partially Completed', 'Partially Completed'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_in_progress', null=True, blank=True)
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_in_progress', null=True, blank=True)
    progress_title = models.CharField(max_length=255, null=True, blank=True)
    progress_date = models.DateField(null=True, blank=True)
    completed_work_details = models.TextField(null=True, blank=True)
    pending_work_details = models.TextField(null=True, blank=True)
    site_inspection_details = models.TextField(null=True, blank=True)
    labour_count = models.IntegerField(null=True, blank=True)
    material_used_details = models.TextField(null=True, blank=True)
    current_site_status = models.TextField(null=True, blank=True)
    delay_reason = models.TextField(null=True, blank=True)
    next_work_plan = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    progress_photo_1 = models.ImageField(upload_to='work_progress/photos/', null=True, blank=True)
    progress_photo_2 = models.ImageField(upload_to='work_progress/photos/', null=True, blank=True)
    progress_photo_3 = models.ImageField(upload_to='work_progress/photos/', null=True, blank=True)
    inspection_report_document = models.FileField(upload_to='work_progress/inspection/', null=True, blank=True)
    milestone_report_document = models.FileField(upload_to='work_progress/milestone/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_progress/other/', null=True, blank=True)
    # System Fields
    updated_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='work_progress_updates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    progress_photo_1 = models.ImageField(upload_to='work_progress/photos/', null=True, blank=True)
    progress_photo_2 = models.ImageField(upload_to='work_progress/photos/', null=True, blank=True)
    progress_photo_3 = models.ImageField(upload_to='work_progress/photos/', null=True, blank=True)
    inspection_report_document = models.FileField(upload_to='work_progress/inspection/', null=True, blank=True)
    milestone_report_document = models.FileField(upload_to='work_progress/milestone/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_progress/other/', null=True, blank=True)
    # System Fields
    updated_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='work_progress_updates', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work In Progress"
        verbose_name_plural = "6.Work In Progress"

    def __str__(self):
        return f"{self.progress_title or ''} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 7 — WORK FINAL
# ─────────────────────────────────────────────────────────────

class Work_Final(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Verified', 'Verified'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_finals', null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    final_work_status = models.TextField(null=True, blank=True)
    final_report = models.TextField(null=True, blank=True)
    completion_remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    final_photo_1 = models.ImageField(upload_to='work_final/photos/', null=True, blank=True)
    final_photo_2 = models.ImageField(upload_to='work_final/photos/', null=True, blank=True)
    final_photo_3 = models.ImageField(upload_to='work_final/photos/', null=True, blank=True)
    completion_certificate_document = models.FileField(upload_to='work_final/certificate/', null=True, blank=True)
    measurement_book_document = models.FileField(upload_to='work_final/measurement/', null=True, blank=True)
    final_report_document = models.FileField(upload_to='work_final/report/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_final/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='work_final_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Final"
        verbose_name_plural = "7.Work Finals"

    def __str__(self):
        return f"{self.work_master} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 8 — PAYMENT PROCESS
# ─────────────────────────────────────────────────────────────

class Payment_Process(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('Advance', 'Advance'),
        ('Mid-Stage', 'Mid-Stage'),
        ('Running Bill', 'Running Bill'),   
        ('Final Payment', 'Final Payment'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processed', 'Processed'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='payment_processes', null=True, blank=True)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    bill_number = models.CharField(max_length=100, null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    payment_remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    bill_document = models.FileField(upload_to='payment_process/bill/', null=True, blank=True)
    invoice_document = models.FileField(upload_to='payment_process/invoice/', null=True, blank=True)
    payment_receipt_document = models.FileField(upload_to='payment_process/receipt/', null=True, blank=True)
    voucher_document = models.FileField(upload_to='payment_process/voucher/', null=True, blank=True)
    other_document = models.FileField(upload_to='payment_process/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='payment_process_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Payment Process"
        verbose_name_plural = "8.Payment Processes"

    def __str__(self):
        return f"{self.payment_type or ''} - {self.payment_amount}"
# ─────────────────────────────────────────────────────────────
# STAGE 9 — PHYSICALLY COMPLETE
# ─────────────────────────────────────────────────────────────

class Physically_Complete(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Inspection Pending', 'Inspection Pending'),
        ('Verified', 'Verified'),
        ('Physically Complete', 'Physically Complete'),
        ('Rejected', 'Rejected'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='physically_completed_works', null=True, blank=True)
    inspection_date = models.DateField(null=True, blank=True)
    inspection_officer_name = models.CharField(max_length=255, null=True, blank=True)
    inspection_remark = models.TextField(null=True, blank=True)
    physical_completion_date = models.DateField(null=True, blank=True)
    verification_status = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    verification_photo_1 = models.ImageField(upload_to='physically_complete/photos/', null=True, blank=True)
    verification_photo_2 = models.ImageField(upload_to='physically_complete/photos/', null=True, blank=True)
    verification_photo_3 = models.ImageField(upload_to='physically_complete/photos/', null=True, blank=True)
    inspection_report_document = models.FileField(upload_to='physically_complete/inspection/', null=True, blank=True)
    completion_certificate_document = models.FileField(upload_to='physically_complete/certificate/', null=True, blank=True)
    officer_verification_letter_document = models.FileField(upload_to='physically_complete/letter/', null=True, blank=True)
    other_document = models.FileField(upload_to='physically_complete/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='physically_complete_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Physically Complete"
        verbose_name_plural = "9.Physically Complete Works"
        verbose_name_plural = "6.Work In Progress"

    def __str__(self):
        return f"{self.progress_title or ''} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 7 — WORK FINAL
# ─────────────────────────────────────────────────────────────

class Work_Final(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
        ('Verified', 'Verified'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='work_finals', null=True, blank=True)
    completion_date = models.DateField(null=True, blank=True)
    final_work_status = models.TextField(null=True, blank=True)
    final_report = models.TextField(null=True, blank=True)
    completion_remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    final_photo_1 = models.ImageField(upload_to='work_final/photos/', null=True, blank=True)
    final_photo_2 = models.ImageField(upload_to='work_final/photos/', null=True, blank=True)
    final_photo_3 = models.ImageField(upload_to='work_final/photos/', null=True, blank=True)
    completion_certificate_document = models.FileField(upload_to='work_final/certificate/', null=True, blank=True)
    measurement_book_document = models.FileField(upload_to='work_final/measurement/', null=True, blank=True)
    final_report_document = models.FileField(upload_to='work_final/report/', null=True, blank=True)
    other_document = models.FileField(upload_to='work_final/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='work_final_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Final"
        verbose_name_plural = "7.Work Finals"

    def __str__(self):
        return f"{self.work_master} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 8 — PAYMENT PROCESS
# ─────────────────────────────────────────────────────────────

class Payment_Process(models.Model):
    PAYMENT_TYPE_CHOICES = (
        ('Advance', 'Advance'),
        ('Mid-Stage', 'Mid-Stage'),
        ('Running Bill', 'Running Bill'),   
        ('Final Payment', 'Final Payment'),
    )
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Processed', 'Processed'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='payment_processes', null=True, blank=True)
    payment_type = models.CharField(max_length=100, choices=PAYMENT_TYPE_CHOICES, null=True, blank=True)
    payment_date = models.DateField(null=True, blank=True)
    payment_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    bill_number = models.CharField(max_length=100, null=True, blank=True)
    invoice_number = models.CharField(max_length=100, null=True, blank=True)
    payment_remark = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    bill_document = models.FileField(upload_to='payment_process/bill/', null=True, blank=True)
    invoice_document = models.FileField(upload_to='payment_process/invoice/', null=True, blank=True)
    payment_receipt_document = models.FileField(upload_to='payment_process/receipt/', null=True, blank=True)
    voucher_document = models.FileField(upload_to='payment_process/voucher/', null=True, blank=True)
    other_document = models.FileField(upload_to='payment_process/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='payment_process_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Payment Process"
        verbose_name_plural = "8.Payment Processes"

    def __str__(self):
        return f"{self.payment_type or ''} - {self.payment_amount}"
# ─────────────────────────────────────────────────────────────
# STAGE 9 — PHYSICALLY COMPLETE
# ─────────────────────────────────────────────────────────────

class Physically_Complete(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Inspection Pending', 'Inspection Pending'),
        ('Verified', 'Verified'),
        ('Physically Complete', 'Physically Complete'),
        ('Rejected', 'Rejected'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='physically_completed_works', null=True, blank=True)
    inspection_date = models.DateField(null=True, blank=True)
    inspection_officer_name = models.CharField(max_length=255, null=True, blank=True)
    inspection_remark = models.TextField(null=True, blank=True)
    physical_completion_date = models.DateField(null=True, blank=True)
    verification_status = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='Pending', null=True, blank=True)
    # Documents
    verification_photo_1 = models.ImageField(upload_to='physically_complete/photos/', null=True, blank=True)
    verification_photo_2 = models.ImageField(upload_to='physically_complete/photos/', null=True, blank=True)
    verification_photo_3 = models.ImageField(upload_to='physically_complete/photos/', null=True, blank=True)
    inspection_report_document = models.FileField(upload_to='physically_complete/inspection/', null=True, blank=True)
    completion_certificate_document = models.FileField(upload_to='physically_complete/certificate/', null=True, blank=True)
    officer_verification_letter_document = models.FileField(upload_to='physically_complete/letter/', null=True, blank=True)
    other_document = models.FileField(upload_to='physically_complete/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='physically_complete_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Physically Complete"
        verbose_name_plural = "9.Physically Complete Works"

    def __str__(self):
        return f"{self.work_master} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 10 — SUCCESS STORY
# ─────────────────────────────────────────────────────────────

class Success_Story(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='success_stories', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    impact_details = models.TextField(null=True, blank=True)
    beneficiary_details = models.TextField(null=True, blank=True)
    before_work_details = models.TextField(null=True, blank=True)
    after_work_details = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft', null=True, blank=True)
    # Documents
    before_photo_1 = models.ImageField(upload_to='success_story/before/', null=True, blank=True)
    before_photo_2 = models.ImageField(upload_to='success_story/before/', null=True, blank=True)
    before_photo_3 = models.ImageField(upload_to='success_story/before/', null=True, blank=True)
    after_photo_1 = models.ImageField(upload_to='success_story/after/', null=True, blank=True)
    after_photo_2 = models.ImageField(upload_to='success_story/after/', null=True, blank=True)
    after_photo_3 = models.ImageField(upload_to='success_story/after/', null=True, blank=True)
    impact_report_document = models.FileField(upload_to='success_story/impact/', null=True, blank=True)
    beneficiary_document = models.FileField(upload_to='success_story/beneficiary/', null=True, blank=True)
    media_coverage_document = models.FileField(upload_to='success_story/media/', null=True, blank=True)
    other_document = models.FileField(upload_to='success_story/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='success_story_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Success Story"
        verbose_name_plural = "91. Success Stories"

    def __str__(self):
        return self.title or ''
    
        return f"{self.work_master} - {self.status}"


# ─────────────────────────────────────────────────────────────
# STAGE 10 — SUCCESS STORY
# ─────────────────────────────────────────────────────────────

class Success_Story(models.Model):
    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Published', 'Published'),
    )
    work_master = models.ForeignKey('Work_Master', on_delete=models.SET_NULL, related_name='success_stories', null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    impact_details = models.TextField(null=True, blank=True)
    beneficiary_details = models.TextField(null=True, blank=True)
    before_work_details = models.TextField(null=True, blank=True)
    after_work_details = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Draft', null=True, blank=True)
    # Documents
    before_photo_1 = models.ImageField(upload_to='success_story/before/', null=True, blank=True)
    before_photo_2 = models.ImageField(upload_to='success_story/before/', null=True, blank=True)
    before_photo_3 = models.ImageField(upload_to='success_story/before/', null=True, blank=True)
    after_photo_1 = models.ImageField(upload_to='success_story/after/', null=True, blank=True)
    after_photo_2 = models.ImageField(upload_to='success_story/after/', null=True, blank=True)
    after_photo_3 = models.ImageField(upload_to='success_story/after/', null=True, blank=True)
    impact_report_document = models.FileField(upload_to='success_story/impact/', null=True, blank=True)
    beneficiary_document = models.FileField(upload_to='success_story/beneficiary/', null=True, blank=True)
    media_coverage_document = models.FileField(upload_to='success_story/media/', null=True, blank=True)
    other_document = models.FileField(upload_to='success_story/other/', null=True, blank=True)
    # System Fields
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='success_story_created_by', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Success Story"
        verbose_name_plural = "91. Success Stories"

    def __str__(self):
        return self.title or ''
    
