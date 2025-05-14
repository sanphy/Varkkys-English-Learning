from django.contrib import admin

from .models import Candidate,AuthUser


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'email',
        'date_of_birth', 'qualification', 'interested_area'
    )

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('username','password')
