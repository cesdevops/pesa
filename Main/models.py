from django.db import models
from django.contrib.auth.hashers import make_password, check_password


class Financial_Year(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )
    year = models.CharField(max_length=20,null=True,blank=True)
    start_date = models.DateField(null=True,blank=True)
    end_date = models.DateField(null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    # def __str__(self):
    #     return self.year if self.year else "Financial Year"
    

class Super_User(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.CharField(max_length=255,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)

    username = models.CharField(max_length=255,unique=True,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    profile = models.ImageField(upload_to='Super_User_Profile/',null=True,blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
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


class District(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "District"


class Taluka(models.Model):
    district = models.ForeignKey('District',on_delete=models.SET_NULL,null=True,blank=True,related_name='talukas')
    name = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)

    def __str__(self):
        return self.name if self.name else "Taluka"





class Kosh_Head(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    name = models.CharField(max_length=255)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Head_Percentage(models.Model):
    kosh_head = models.ForeignKey(
        Kosh_Head,
        on_delete=models.CASCADE,
        related_name='head_percentages'
    )
    percentage = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.kosh_head.name} - {self.percentage}%"


