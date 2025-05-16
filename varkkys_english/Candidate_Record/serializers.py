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
        ]
