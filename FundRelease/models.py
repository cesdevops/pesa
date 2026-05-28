from django.db import models
from Main.models import Financial_Year ,Kosh_Head
from Kosh.models import Kosh
from ZillaParishad.models import Zilla_Parishad, Zilla_Parishad_User

class Fund_Release(models.Model):
    financial_year = models.ForeignKey(
        Financial_Year,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    zilla_parishad = models.ForeignKey(
        Zilla_Parishad,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fund_releases'
    )
    added_by = models.ForeignKey(
        Zilla_Parishad_User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fund_release_added_by'
    )
    release_name = models.CharField(max_length=200, null=True, blank=True)
    installment = models.CharField(max_length=20, null=True, blank=True)
    release_order_no = models.CharField(max_length=100, unique=True, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    total_amount = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True)
    fund_distributed = models.BooleanField(default=False)
    remarks = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return f"{self.release_name} - {self.release_order_no}"


class Kosh_Fund_Allocation(models.Model):

    STATUS_CHOICES = (
        ('Allocated', 'Allocated'),
        ('Partially Used', 'Partially Used'),
        ('Fully Used', 'Fully Used'),
        ('Lapsed', 'Lapsed'),
    )

    fund_release = models.ForeignKey("Fund_Release", on_delete=models.SET_NULL, related_name='kosh_fund_allocations', null=True,blank=True)
    kosh = models.ForeignKey(Kosh, on_delete=models.SET_NULL, related_name='fund_allocations', null=True,blank=True)
    allocated_amount = models.DecimalField( max_digits=15, decimal_places=2, default=0)
    released_amount = models.DecimalField( max_digits=15, decimal_places=2, default=0)
    balance_amount = models.DecimalField( max_digits=15,decimal_places=2,default=0)
    total_lapsed_amount = models.DecimalField( max_digits=15,decimal_places=2,default=0)
    allocated_date = models.DateField()
    status = models.CharField( max_length=30,choices=STATUS_CHOICES, default='Allocated')
    remark = models.TextField(null=True, blank=True)
    is_fund_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kosh} - {self.allocated_amount}"

    class Meta:
        verbose_name = "Kosh Fund Allocation"
        verbose_name_plural = "Kosh Fund Allocations"
        ordering = ['-created_at']




class HeadAllocation(models.Model):
    kosh_fund_allocation = models.ForeignKey(
        Kosh_Fund_Allocation,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='head_allocations'
    )
    kosh_head = models.ForeignKey(
        Kosh_Head,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='head_allocations'
    )
    allocated_amount = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    utilize_amount = models.DecimalField(max_digits=15,decimal_places=2,default=0 )
    lapsed_amount = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    freezed_amount = models.DecimalField(max_digits=15,decimal_places=2,default=0)
    remaining_amount = models.DecimalField( max_digits=15,decimal_places=2,default=0 )
    is_fund_given = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kosh_head} - {self.allocated_amount}"

    class Meta:
        verbose_name = "Head Allocation"
        verbose_name_plural = "Head Allocations"
        ordering = ['-created_at']