import uuid
from django.contrib import auth
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, User
from django.core.validators import RegexValidator

# Create your models here.


class Account(AbstractBaseUser):
    id = models.IntegerField(unique=True, primary_key=True)
    username = models.CharField(unique=True,max_length = 35)
    auth_id = models.CharField(max_length = 35)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def to_Dict(self):

        data = {}
        try:
            if(self.id):
                data["id"] = self.id
            if(self.username):
                data["username"] = self.username
            if(self.auth_id):
                data["auth_id"] = self.auth_id
            return data
        except:
            return {}


class PhoneNumber(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    number = models.CharField(validators=[phone_regex], max_length=17, blank=True) 
    account = models.ForeignKey(Account, null=True, on_delete=models.DO_NOTHING)



    def to_Dict(self):

        data = {}
        try:
            if(self.number):
                data["number"] = self.number
            if(self.account):
                data["account"] = self.account
            return data
        except:
            return {}