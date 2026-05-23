from django.db import models
from django.contrib.auth.hashers import make_password, check_password

from Main.models import District

class Zilla_Parishad(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    zillaParishad_name = models.CharField(max_length=255,null=True,blank=True)
    district = models.ForeignKey(District,on_delete=models.SET_NULL,null=True,blank=True,related_name='zilla_parishads')
    zillaParishad_code = models.CharField(max_length=50,unique=True,null=True,blank=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True,null=True,blank=True)
    updated_at = models.DateTimeField(auto_now=True,null=True,blank=True)


class Zilla_Parishad_User(models.Model):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
    )

    zilla_parishad = models.ForeignKey(Zilla_Parishad,on_delete=models.SET_NULL,null=True,blank=True, related_name='zp_users')
    zilla_parishad_name = models.CharField(max_length=255,null=True,blank=True)
    name = models.CharField(max_length=255,null=True,blank=True)
    
    mobile = models.CharField(max_length=20,null=True,blank=True)
    email = models.EmailField(null=True,blank=True)
    address = models.TextField(null=True,blank=True)
    Role = models.CharField(max_length=255,null=True,blank=True)

    username = models.CharField(max_length=255,unique=True,null=True,blank=True)
    password = models.CharField(max_length=255,null=True,blank=True)
    profile = models.ImageField(upload_to='ZillaParishad_User_Profile/',null=True,blank=True)

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

