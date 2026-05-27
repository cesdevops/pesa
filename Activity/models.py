from django.db import models
from Kosh.models import Kosh_User

class Administrative_Sanction(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Submitted', 'Submitted'),
        ('Rejected', 'Rejected'),
    )
    activity = models.CharField(max_length=255, null=True, blank=True)
    sanction_number = models.CharField(max_length=100, null=True, blank=True)
    work_name = models.CharField(max_length=255, null=True, blank=True)
    work_description = models.TextField(null=True, blank=True)
    department_name = models.CharField(max_length=255, null=True, blank=True)
    estimated_amount = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    approved_amount = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    sanction_date = models.DateField(null=True, blank=True)
    proposal_date = models.DateField(null=True, blank=True)
    work_location = models.CharField(max_length=255, null=True, blank=True)
    objective = models.TextField(null=True, blank=True)
    beneficiary_details = models.TextField(null=True, blank=True)
    resolution_number = models.CharField(max_length=100, null=True, blank=True)
    resolution_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending',null=True,blank=True)
    created_by = models.ForeignKey(Kosh_User,on_delete=models.SET_NULL,related_name='administrative_sanctions',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Administrative Sanction"
        verbose_name_plural = "Administrative Sanctions"

    def __str__(self):
        return f"{self.sanction_number} - {self.work_name}"

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
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE, related_name='technical_sanctions', null=True, blank=True)
    administrative_sanction = models.ForeignKey('Administrative_Sanction', on_delete=models.SET_NULL, related_name='technical_sanctions', null=True, blank=True)
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
    created_by = models.ForeignKey(Kosh_User, on_delete=models.SET_NULL, related_name='technical_sanctions', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    class Meta:
        ordering = ['-id']
        verbose_name = "Technical Sanction"
        verbose_name_plural = "Technical Sanctions"

    def __str__(self):
        return f"{self.technical_sanction_number} - {self.activity}"





class Work_Order(models.Model):

    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        # ('Approved', 'Approved'),
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )

    # kosh = models.ForeignKey(
    #     'Kosh',
    #     on_delete=models.SET_NULL,
    #     null=True,
    #     blank=True,
    #     related_name='work_orders'
    # )
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
    estimated_amount = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    approved_amount = models.DecimalField(max_digits=15,decimal_places=2,null=True,blank=True)
    category = models.CharField(max_length=100,null=True,blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending',null=True,blank=True)
    remarks = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(Kosh_User,on_delete=models.SET_NULL,related_name='created_work_orders',null=True,blank=True)
    updated_by = models.ForeignKey(Kosh_User,on_delete=models.SET_NULL,related_name='updated_work_orders',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Order"
        verbose_name_plural = "Work Orders"

    def __str__(self):
        return f"{self.work_order_number} - {self.work_name}"

class Work_Start(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Started', 'Started'),
        ('On Hold', 'On Hold'),
        ('Completed', 'Completed'),
    )

    start_date = models.DateField(null=True, blank=True)
    expected_end_date = models.DateField(null=True, blank=True)
    actual_start_date = models.DateField(null=True, blank=True)
    site_location = models.CharField(max_length=255, null=True, blank=True)
    supervisor_name = models.CharField(max_length=255, null=True, blank=True)
    contractor_name = models.CharField(max_length=255, null=True, blank=True)
    initial_work_status = models.TextField(null=True, blank=True)
    remarks = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending',null=True,blank=True)
    started_by = models.ForeignKey(Kosh_User,on_delete=models.SET_NULL,related_name='started_works',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work Start"
        verbose_name_plural = "Work Starts"

    def __str__(self):
        return f"{self.contractor_name} - {self.status}"
    

class Work_In_Progress(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('In Progress', 'In Progress'),
        ('Partially Completed', 'Partially Completed'),
        ('Completed', 'Completed'),
        ('On Hold', 'On Hold'),
    )

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
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='Pending',null=True,blank=True)
    updated_by = models.ForeignKey(Kosh_User,on_delete=models.SET_NULL,related_name='work_progress_updates',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    class Meta:
        ordering = ['-id']
        verbose_name = "Work In Progress"
        verbose_name_plural = "Work In Progress"

    def __str__(self):
        return f"{self.progress_title} - {self.status}"



