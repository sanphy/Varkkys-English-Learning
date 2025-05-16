from django.contrib import admin
from django.contrib.auth.models import User
from .models import Candidate
from django.contrib.auth.admin import UserAdmin


admin.site.unregister(User)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone','email',
         'qualification', 'interested_area','status','remarks','assigned_to'
    )
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)



