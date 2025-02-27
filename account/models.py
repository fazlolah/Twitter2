from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.crypto import get_random_string
# from core.models import *

# Create your models here.

class User(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=11, unique=True, blank=True, null=True)
    email_active_code = models.CharField(max_length=64, default=get_random_string(64))
    is_email_activated = models.BooleanField(default=False)
    is_phone_number_activated = models.BooleanField(default=False)
    date_of_birth = models.DateField(null=True, blank=True)    
    location = models.TextField(null=True, blank=True)
    
    # Gender field with corrected choices format
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('N', 'Prefer not to say'),
    ]
    
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N')
    
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', default='images/no_pfp.png')
    cover_picture = models.ImageField(upload_to='cover_pictures/', blank=True, null=True)

    
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.get_full_name() or self.username

    def get_joined_date(self):
        return self.created_at.strftime('%b %Y')

    # def get_tweets(self):
    #     tweets = Tweet.objects.filter(id=self.id)
    #     return tweets