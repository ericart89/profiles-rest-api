from django.db import models

# standard base classes that we overwrite when we customize the standard User model of django
# this is described in the documentation of Django
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

#for the manager
from django.contrib.auth.models import BaseUserManager


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""
    #if the password is not specified, it will default to None
    #a None password won't work because it needs to be a hash
    #hence, until you set a password you cannot authenticate
    def create_user(self,email,name,password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')
        #for upper letters:
        email = self.normalize_email(email)
        user = self.model(email=email, name=name)
        #we dont pass the password before because we wanna make sure
        #that the password is encrypted. We want to make sure that the
        #password is converted to a hash and not store as plain text in the DB
        #django encrypts with the setpassword function
        user.set_password(password)
        #the standard is to specify the db that you want to use
        #django can support multiple dbs
        user.save(using=self._db)

        return user

    def create_superuser(self,email,name, password):
        """Create and save a new superuser with given details"""
        user=self.create_user(email, name, password)

        user.is_superuser= True
        user.is_staff= True
        user.save(using=self._db)
        return user




# Create your models here.
class UserProfile(AbstractBaseUser,PermissionsMixin):
    """Database model for users in the system"""
    # we want a column in the db corresponding to the email
    # maximum length of 255 characters
    email = models.EmailField(max_length=255,unique=True)
    name = models.CharField(max_length=255)

    # fields for the permission system:
    # the first is to check if the user profile is activated or not
    is_active= models.BooleanField(default=True)
    #if its staff they should have access to the django admin
    is_staff= models.BooleanField(default=False)

    # we need to specify the model manager that we use for the objects
    # we need to use our custom model with Django CLI
    # django needs a custom model manager for user so it knows how to create users

    objects = UserProfileManager()

    # this is to work with django admin and authentication system:
    # we are overwriting the default username and replace it with the email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS=['name']

    # functions that are used by django to interact with our custom model:
    def get_full_name(self):
        """Retrieve full name of user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name

    #the equivalent of java toString:
    def __str__(self):
        """Return string representation of our user"""
        return  self.email

