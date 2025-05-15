from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.hashers import make_password, check_password


class AuthUser(models.Model):
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # hashed password

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def save(self, *args, **kwargs):
        # Hash the password only if it's not already hashed
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


class Candidate(models.Model):
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('not-interested', 'Not-interested'),
        ('followup', 'followup'),
        ('rejected', 'Rejected'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        primary_key=True,
        validators=[RegexValidator(
            regex=r'^[6-9]\d{11}$',
            message="Phone number must be exactly 12 digits and start with 6, 7, 8, or 9."
        )],
        help_text="Unique phone number (12 digits)."
    )
    email = models.EmailField(unique=True)
    address = models.TextField(blank=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True)
    interested_area = models.CharField(
        max_length=255,
        blank=True,
        help_text="E.g. Data Science, Web Dev, AI"
    )

    current_role = models.CharField(max_length=100, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='interested')
    remarks = models.TextField(blank=True)
    requirements_of_candidate = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
