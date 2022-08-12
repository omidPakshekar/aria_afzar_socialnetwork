import string 
import random

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db.models.signals import (pre_save, post_save)
from django.dispatch import receiver

COUNTRY_CHOICES = (
        ('IR', 'Iran'),
        ('US', 'United State'),
        ('UK', 'United Kindom'),
        ('CH', 'China'),
        ('BR', 'Brazil'),
        ('FR', 'French'),
        ('PL', 'Poland'),
)

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

MONTH_CHOICE = (
    ( '1', '1 Month'),
    ('3', '3 Month'),
    ('6', '6 Month'),
    ('12', '12 Month'),
    
)
def get_profile_image_filepath(self, filename):
    return f'profile_images/{self.username + ".png"}'

def get_default_profile_image():
    return "students/default_profile_image.png"

def create_wallet_key():
    # lenght of key
    length = 28
    # chose what charecter we want 
    letters = string.ascii_letters
    number = ''.join([str(i) for i in range(0, 10)])
    charecter = letters + number 
    # the final key is like = 'wallet(key)' 
    return  'wallet_' + ''.join(random.choice(charecter) for i in range(length))


class MyAccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)

		user.set_password(password)
		user.save()
		return user

	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save()
		return user

class CustomeUserModel(AbstractBaseUser, PermissionsMixin):
    class Meta:
        verbose_name_plural = 'users'
    
    email 				= models.EmailField(verbose_name="email", max_length=60, unique=True)
    username 			= models.CharField(max_length=30, unique=True)
    date_joined			= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login			= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin			= models.BooleanField(default=False)
    is_active			= models.BooleanField(default=True)
    is_staff			= models.BooleanField(default=False)
    is_superuser		= models.BooleanField(default=False)
    profile_image       = models.ImageField(max_length=255, upload_to=get_profile_image_filepath, null=True, blank=True, default=get_default_profile_image)
    hide_email          = models.BooleanField(default=True)
    gender              = models.CharField(max_length=1, choices=GENDER_CHOICES)
    country             = models.CharField(max_length=20, choices=COUNTRY_CHOICES)
    activity            = models.IntegerField(default=0)
    objects = MyAccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.username
    
    # def has_perm(self, perm, obj=None):
    #     return self.is_admin

    def get_profile_image_filename(self):
        return str(self.profile_image)[str(self.profile_image).index(f"profile_images/{self.pk}"):]
	
	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    # def has_module_perms(self, app_label):
    # 	return True


class Wallet(models.Model):
    owner = models.OneToOneField(CustomeUserModel, related_name='wallet', on_delete=models.CASCADE)
    amount = models.DecimalField(default=0, decimal_places=2, max_digits=10)
    wallet_key = models.CharField(max_length=35, editable=False,
            default=create_wallet_key , blank=False, null=False)
    created_time = models.DateTimeField(auto_now_add = True)
    updated_time = models.DateTimeField(auto_now = True)
    
    def __str__(self) -> str:
         return self.owner.username + " wallet"

"""
    signal -- we use signal to create wallet automaticly after user created
"""
@receiver(post_save, sender=CustomeUserModel)
def user_post_save_receiver(sender, instance, created, *args, **kwargs):
    """
    after saved in the database
    """
    if created:
        # send email with celery
        print("Send email to", instance.username)
        # create wallet 
        wallet = Wallet(owner=instance)
        wallet.save()


class MemberShip(models.Model):
    user    = models.OneToOneField(CustomeUserModel, related_name='membership',  on_delete=models.CASCADE)
    month   =  models.CharField(max_length=20, choices=MONTH_CHOICE)
    amount  = models.DecimalField(blank=True, decimal_places=2, max_digits=10)
    started_date =  models.DateTimeField(verbose_name='date_create', auto_now_add=True)  
    expired_day = models.IntegerField(default=0)

"""
    signal -- create expire day and amount automaticly  
"""
@receiver(pre_save, sender=MemberShip)
def blog_post_pre_save(sender, instance, *args, **kwargs):
    if instance.amount == None:
        if instance.month == '1':
            instance.amount = 24.87
            instance.expired_day = 30
        elif instance.month == '3':
            instance.amount = 64.47
            instance.expired_day = 90
        elif instance.month == '6':
            instance.amount = 117.47
            instance.expired_day = 180
        else:
            instance.amount = 238.87
            instance.expired_day = 360
        instance.save()








