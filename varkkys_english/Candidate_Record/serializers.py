from rest_framework import serializers
from .models import Candidate,AuthUser

class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Candidate
        fields = ['first_name', 'last_name', 'phone', 'email','address','age','qualification',
                  'interested_area','current_role','status','remarks','requirements_of_candidate']
class AuthUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuthUser
        fields = '__all__'
