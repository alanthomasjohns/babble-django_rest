from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, AbstractUser
from django.conf import settings
from user.manager import UserManager
from django.core.validators import RegexValidator




# Create your models here.


# class AccountManager(BaseUserManager) :
#     def create_user(self, first_name, last_name, email, username, gender, dob, password=None) :
#         if not first_name :
#             raise ValueError("User must provide the first name")
#         if not email :
#             raise ValueError("User must provide an email")
#         if not username :
#             raise ValueError("User must provide a username")
#         if not gender :
#             raise ValueError("User must provide the gender")
#         if not dob :
#             raise ValueError("User must provide date of birth")
        
        
#         user = self.model(
#             email = self.normalize_email(email),
#             first_name = first_name,
#             last_name = last_name,
#             username = username,
#             gender = gender,
#             dob = dob
#         )
#         user.set_password(password)
#         user.save()
        
#         return user
    
#     def create_superuser(self, first_name, last_name, email, username, gender, dob, password) :
#         user = self.create_user(
#             email=self.normalize_email(email),
#             first_name=first_name,
#             last_name=last_name,
#             username= username,
#             dob=dob,
#             gender=gender,
#             password=password
#         )
        
#         user.is_admin = True
#         user.is_staff = True
#         user.is_superuser = True
        
#         user.save()
#         return user
        
        

class Account(AbstractUser):

    gender_choices = (
        ('Female', 'Female'),
        ('Male', 'Male'),
        ('Custom', 'Custom')
    )
    username = models.CharField(max_length=14, null=True)
    first_name = models.CharField(max_length=14)
    last_name = models.CharField(max_length=14)
    email = models.EmailField( unique=True)
    account_type = models.CharField('Account Type',
                                    max_length=8,
                                    blank=True,
                                    default='PERSONAL',
                                    choices=[('BUSINESS', 'Business'), ('PERSONAL', 'Personal')])
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL,
                                       related_name='Follower',
                                       blank=True,
                                       symmetrical=False)
    # following = models.ManyToManyField(settings.AUTH_USER_MODEL,
    #                                    related_name='Followinggg',
    #                                    blank=True,
    #                                    symmetrical=False)
    is_private = models.BooleanField(default=False)
    is_deactivated = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=6 , null=True, blank=True)
    
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    
    def name(self):
        return self.first_name + ' ' + self.last_name

    def __str__(self):
        return self.email



class UserProfile(models.Model):

    GENDER_CHOICES = (
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other')
)

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birthday = models.DateField(null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null = True)
    profile_pic = models.ImageField(default='default_user.jfif', upload_to = 'profile_pics')
    cover_pic = models.ImageField(default='default_cover.jfif', upload_to = 'cover_pics')
    account_type = models.CharField('Account Type',
                                    max_length=8,
                                    blank=True,
                                    default='PERSONAL',
                                    choices=[('BUSINESS', 'Business'), ('PERSONAL', 'Personal')])
    bio = models.TextField(blank=True)
    is_private = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=10, blank=True, unique = True,
                                    validators=[RegexValidator(regex='^[0-9]{10}$', message='Enter a 10 digit phone number.',),])
    profile_image = models.ImageField(upload_to="profile_image", null=True, blank=True) 
    is_online = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
