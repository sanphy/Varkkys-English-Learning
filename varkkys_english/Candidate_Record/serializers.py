from rest_framework import serializers
from .models import Candidate
from django.contrib.auth.models import User


class CandidateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.filter(is_staff=True),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Candidate
        fields = [

            'first_name',
            'last_name',
            'phone',
            'email',
            'address',
            'age',
            'qualification',
            'interested_area',
            'current_role',
            'status',
            'remarks',
            'requirements_of_candidate',
            'assigned_to',
            'audio_record',
            "lead_type"
        ]

    def validate_phone(self, value):
        """
        Clean and validate phone number:
        - Remove spaces, hyphens, parentheses
        - Allow optional '+' at the start
        - Ensure max 12 digits after optional '+'
        """
        # Remove unwanted characters
        cleaned = value.replace(" ", "").replace("-", "").replace("(", "").replace(")", "")

        # Handle optional '+' at the beginning
        if cleaned.startswith('+'):
            digits = cleaned[1:]
        else:
            digits = cleaned

        if not digits.isdigit():
            raise serializers.ValidationError("Phone number must contain only digits after optional '+'.")

        if len(digits) > 12:
            raise serializers.ValidationError("Phone number must be up to 12 digits (excluding optional '+').")

        return cleaned