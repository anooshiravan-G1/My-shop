from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    zip_code = models.CharField(max_length=10, blank=True)
    is_active = models.BooleanField(default=False)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',  
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
    )
    
    # Fields required for authentication
    REQUIRED_FIELDS = ['email', 'password']
    USERNAME_FIELD = 'email'


    def __str__(self):
        return self.username
    
    def get_username(self):
        return self.email

    def set_password(self, raw_password):
        # Your password hashing logic here
        super().set_password(raw_password)

    def check_password(self, raw_password):
        # Your password checking logic here
        return super().check_password(raw_password)

