from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .managers import CustomUserManager


########## FOR FILE UPLOAD ###############################3
import os
from CheffyBackend.settings import BASE_DIR
from django.conf import settings
from django.core.files.storage import FileSystemStorage

fs = FileSystemStorage(location=os.path.join(BASE_DIR, "media"))
###########################################################

class CustomUser(AbstractUser):
    username = None
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{10,10}$', message="Phone number must be entered without country code:Example '9876543210'")
    phone_number = models.CharField(validators=[
        phone_regex], max_length=10, unique=True, blank=False)  # validators should be a list
    user_type = models.IntegerField(default=0)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        if(self.user_type == 1):
            st = "Customer"
        else:
            st = "Partner"
        return str(self.id) + ". phone no. " + self.phone_number + ", usertype = " + st



class CustomerProfile(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), unique=True, blank=False)
    fullname = models.CharField(max_length=50, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=False)

    address = models.TextField(blank=True, unique=False)
    flat_no = models.CharField(max_length=255, blank=True)
    landmark = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return "user " + str(self.user.id) + " " + self.user.phone_number + " " + self.fullname


class PartnerProfile(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    email = models.EmailField(_('email address'), unique=True, blank=False)
    fullname = models.CharField(max_length=50, blank=False)
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES, blank=False)

    qualification = models.CharField(max_length=255)
    # qualification_doc = models.FileField(upload_to='qualification_doc', storage=fs,blank=True)
    place_of_work = models.CharField(max_length=512)
    #place_of_work_doc = models.FileField(upload_to='place_of_work_doc', storage=fs,blank=True)
    yex = models.IntegerField()

    def __str__(self):
        return "user " + str(self.user.id) + ": " + self.user.phone_number + ", " + self.fullname


class OTP(models.Model):
    phone_number = models.CharField(max_length=10, blank=False, unique=True)
    otp = models.CharField(max_length=6, blank=False)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id) + ". phone no." + self.phone_number + ", otp=" + self.otp + " isVerified=" + str(self.is_verified)


# class chlumodel(models.Model):
#     f = models.FileField()


class Cordinates(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE)
    lat = models.CharField(max_length=20)
    lon = models.CharField(max_length=20)

    def __str__(self):
        return self.user.phone_number + " " +self.lat + " " + self.lon