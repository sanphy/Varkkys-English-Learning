from rest_framework import serializers
from .models import Candidate
from django.contrib.auth.models import User


class CandidateSerializer(serializers.ModelSerializer):
    assigned_to = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Candidate
        fields = '__all__'