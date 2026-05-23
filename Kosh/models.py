from django.db import models
from Main.models import Financial_Year
from PanchayatSamiti.models import Panchayat_Samiti
from django.contrib.auth.hashers import make_password, check_password

class GramPanchayat(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    panchayat_samiti = models.ForeignKey(Panchayat_Samiti,on_delete=models.SET_NULL,null=True,blank=True, related_name='gram_panchayats')
    panchayat_samiti_name = models.CharField(max_length=255,null=True,blank=True)
    gram_panchayat_name = models.CharField(max_length=255,null=True,blank=True)
    gram_panchayat_code = models.CharField(max_length=50,unique=True,null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.gram_panchayat_name if self.gram_panchayat_name else "Gram Panchayat"
    

class Kosh(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Closed', 'Closed'),
    )

    gramPanchayat = models.ForeignKey('GramPanchayat',on_delete=models.SET_NULL,null=True,blank=True, related_name='kosh')
    gramPanchayat_name = models.CharField(max_length=255,null=True,blank=True)
    kosh_name = models.CharField(max_length=255,null=True,blank=True)
    kosh_code = models.CharField(max_length=100,unique=True,null=True,blank=True)
    is_primary = models.BooleanField(default=False,null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    
    is_deleted = models.BooleanField(default=False,null=True,blank=True)
    deleted_date = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.kosh_name if self.kosh_name else "Kosh"

class Kosh_Cast_Category(models.Model):
    category_name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.category_name if self.category_name else "Cast Category"

class Kosh_Population(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    gram_panchayat = models.ForeignKey('GramPanchayat',on_delete=models.SET_NULL,null=True,blank=True,related_name='kosh_populations')
    cast_category = models.ForeignKey('Kosh_Cast_Category',on_delete=models.SET_NULL,null=True,blank=True,related_name='kosh_populations')
    financial_year = models.ForeignKey(Financial_Year,on_delete=models.SET_NULL,null=True,blank=True,related_name='kosh_populations')
    population_count = models.BigIntegerField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.gram_panchayat} - {self.cast_category} - {self.population_count}"


class Kosh_Total_Population(models.Model):
    kosh = models.ForeignKey('Kosh',on_delete=models.SET_NULL,null=True,blank=True, related_name='kosh_total_populations')
    financial_year = models.ForeignKey(Financial_Year,on_delete=models.SET_NULL,null=True,blank=True,related_name='kosh_total_populations')
    total_population = models.BigIntegerField(null=True,blank=True)
    tribal_population = models.BigIntegerField(null=True,blank=True)
    created = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return f"{self.kosh} - {self.financial_year}"

class Kosh_User(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    kosh = models.ForeignKey('Kosh',on_delete=models.SET_NULL,null=True,blank=True, related_name='kosh_users')
    kosh_name = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)

    username = models.CharField(max_length=255,unique=True,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    profile = models.ImageField(upload_to='Kosh_User_Profile/',null=True,blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    is_retired = models.BooleanField(default=False,null=True,blank=True)
    retired_on = models.DateTimeField(null=True,blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.name if self.name else "Kosh User"

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)


class Kosh_Committee(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    ROLE_CHOICES = (
        ('Chairman', 'Chairman'),
        ('Member', 'Member'),
    )

    kosh = models.ForeignKey('Kosh',on_delete=models.SET_NULL,null=True,blank=True, related_name='committee_members')
    kosh_name = models.CharField(max_length=255,null=True,blank=True)
    role = models.CharField(max_length=50,choices=ROLE_CHOICES,null=True,blank=True)

    name = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)

    profile = models.ImageField(upload_to='Kosh_Committee_Profile/',null=True,blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def __str__(self):
        return self.name if self.name else "Kosh Committee"

class Kosh_Bank_Detail(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Closed', 'Closed'),
    )
    kosh = models.ForeignKey('Kosh',on_delete=models.SET_NULL,null=True,blank=True,related_name='kosh_bank_details')
    kosh_name = models.CharField(max_length=255,null=True,blank=True)
    bank_name = models.CharField(max_length=255,null=True,blank=True)
    branch_name = models.CharField(max_length=255,null=True,blank=True)
    account_holder_name = models.CharField(max_length=255,null=True,blank=True)
    account_number = models.CharField(max_length=100,null=True,blank=True)
    ifsc_code = models.CharField(max_length=20,null=True,blank=True)
    account_type = models.CharField(max_length=50,null=True,blank=True)
    opening_balance = models.DecimalField(max_digits=15,decimal_places=2,default=0,null=True,blank=True)
    current_balance = models.DecimalField(max_digits=15,decimal_places=2,default=0,null=True,blank=True)
    bank_address = models.TextField(null=True,blank=True)








