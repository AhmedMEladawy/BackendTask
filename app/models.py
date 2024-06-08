
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='employee')
    email_regex = RegexValidator(
        regex=r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        message="Please enter a valid email address."
    )
    email = models.EmailField(unique=True, validators=[email_regex])


    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Company(models.Model):
    name = models.CharField(max_length=255)
    number_of_departments = models.IntegerField(default=0)
    number_of_employees = models.IntegerField(default=0)

class Department(models.Model):
    company = models.ForeignKey(Company, related_name='departments', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    number_of_employees = models.IntegerField(default=0)

class Employee(models.Model):
    STATUS_CHOICES = (
        ('onboarding', 'Onboarding'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    company = models.ForeignKey(Company, related_name='employees', on_delete=models.CASCADE)
    department = models.ForeignKey(Department, related_name='employees', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='onboarding')
    name = models.CharField(max_length=255)
    email_regex = RegexValidator(
        regex=r'^[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$',
        message="Please enter a valid email address."
    )
    email = models.EmailField(unique=True, validators=[email_regex])
    
    mobile_regex = RegexValidator(
        regex=r'^01\d{9}$',
        message="Mobile number must be 11 digits and start with 01."
    )
    mobile_number = models.CharField(max_length=11, validators=[mobile_regex])

    address = models.TextField()
    designation = models.CharField(max_length=255)
    hired_on = models.DateField(null=True, blank=True)
    days_employed = models.IntegerField(null=True, blank=True)

    def clean(self):
        if self.status == 'active':
            if not self.hired_on:
                raise ValidationError({'hired_on': 'This field is required when status is active.'})
            if self.days_employed is None:
                raise ValidationError({'days_employed': 'This field is required when status is active.'})
        elif self.status == 'onboarding':
            if self.hired_on or self.days_employed:
                raise ValidationError({'non_field_errors': 'hired_on and days_employed should only be set when status is active.'})
        else:
            self.hired_on = None
            self.days_employed = None

    def save(self, *args, **kwargs):
        self.full_clean()  
        if self.status == 'active' and self.hired_on:
            self.days_employed = (timezone.now().date() - self.hired_on).days
        else:
            self.hired_on = None
            self.days_employed = None
        super().save(*args, **kwargs)
