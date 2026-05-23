from django.db import models
from Main.models import Taluka
from ZillaParishad.models import Zilla_Parishad
from django.contrib.auth.hashers import make_password, check_password

class Panchayat_Samiti(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    zilla_parishad = models.ForeignKey(Zilla_Parishad,on_delete=models.SET_NULL,null=True,blank=True, related_name='panchayat_samitis')
    zilla_parishad_name = models.CharField(max_length=255,null=True,blank=True)
    panchayat_samiti_name = models.CharField(max_length=255,null=True,blank=True)
    panchayat_samiti_code = models.CharField(max_length=255,unique=True,null=True,blank=True)
    taluka = models.ForeignKey(Taluka,on_delete=models.SET_NULL,null=True,blank=True,related_name='panchayat_samitis')
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

class Panchayat_Samiti_User(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    panchayat_samiti = models.ForeignKey('Panchayat_Samiti',on_delete=models.SET_NULL,null=True,blank=True, related_name='panchayat_samiti_users')
    name = models.CharField(max_length=255,null=True,blank=True)
    mobile = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    role = models.CharField(max_length=255,null=True,blank=True)

    username = models.CharField(max_length=255,unique=True,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    profile = models.ImageField(upload_to='Panchayat_Samiti_User_Profile/',null=True,blank=True)

    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    is_retired = models.BooleanField(default=False,null=True,blank=True)
    retired_on = models.DateTimeField(null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)  




