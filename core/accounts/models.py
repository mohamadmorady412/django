from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _

class UserManager(BaseUserManager):
    """the pussy"""
    def creat_user(self, email, password, **extra_filds):
        if not email:
            raise ValueError(_("email must be set!"))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_filds)
        user.set_password(password)
        user.save()
        return user
    def create_superuser(self, email, password, **extra_filds):
        extra_filds.setdefault("is_staff", True)
        extra_filds.setdefault("is_superuser", True)
        extra_filds.setdefault("is_active", True)
        
        if extra_filds.get("is_staff") is not True:
            raise ValueError(_("super user must be staff"))
        if extra_filds.get("is_superuser") is not True:
            raise ValueError(_("super user must be su true"))
        
        return self.creat_user(email, password, **extra_filds)

class User(AbstractBaseUser, PermissionsMixin):
    """"custom user model for our app"""
    email = models.EmailField(max_length=255, unique=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    #is_vrifid = models.BooleanField(default=False)
    first_name = models.CharField(max_length=20)

    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = []
    
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    objects = UserManager()
    def __str__(self):
        return self.email

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    image = models.ImageField(blank=True, null=True)
    description = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email

@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created: Profile.objects.create(user=instance)
