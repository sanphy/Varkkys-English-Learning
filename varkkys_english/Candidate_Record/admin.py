from django.contrib import admin

from .models import Candidate,AuthUser


@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone','email',
         'qualification', 'interested_area','status','remarks'
    )

@admin.register(AuthUser)
class AuthUserAdmin(admin.ModelAdmin):
    list_display = ('username','password')
