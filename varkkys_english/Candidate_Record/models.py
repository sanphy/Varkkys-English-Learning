from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import User


class Candidate(models.Model):
    STATUS_CHOICES = [
        ('interested', 'Interested'),
        ('not-interested', 'Not-interested'),
        ('followup', 'Followup'),
        ('rejected', 'Rejected'),
    ]
    STATUS_CHOICES_LEAD = [
        ('inbound_lead', 'Inbound Lead'),
        ('outbound_lead', 'Outbound Lead'),
    ]

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(
        max_length=15,
        primary_key=True
    )
    email = models.EmailField(blank=True,null=True)
    address = models.TextField(blank=True,null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    qualification = models.CharField(max_length=255, blank=True,null=True)
    interested_area = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="E.g. Data Science, Web Dev, AI"
    )
    current_role = models.CharField(max_length=100, blank=True,null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='interested')
    remarks = models.TextField(blank=True,null=True)
    requirements_of_candidate = models.TextField(blank=True,null=True)
    assigned_to = models.ForeignKey(
        User,  # using Django’s User model
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={'is_staff': True},)  # directly use role field on User
        # filter only staff    created_at = models.DateTimeField(auto_now_add=True)
    # audio_record = models.FileField(upload_to='audio_records/', blank=True, null=True)
    lead_type = models.CharField(max_length=20, choices=STATUS_CHOICES_LEAD, default='outbound_lead')
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# models.py
class CandidateAudioRecord(models.Model):
    candidate = models.ForeignKey(Candidate, related_name='audio_records', on_delete=models.CASCADE)
    original_filename = models.CharField(max_length=255,blank=True,null=True)  # NEW FIELD to store original file name
    audio_file = models.FileField(upload_to='audio_records/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio for {self.candidate.phone} - {self.audio_file.name}"
