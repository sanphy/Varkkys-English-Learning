from django.contrib import admin
from django.contrib.auth.models import User
from .models import Candidate
from django.contrib.auth.admin import UserAdmin
import pandas as pd
from django.contrib import admin, messages
from django.urls import path
from django.shortcuts import render, redirect
from .models import Candidate
from .forms import ExcelUploadForm


admin.site.unregister(User)

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = (
        'first_name', 'last_name', 'phone','email',
         'qualification', 'interested_area','status','remarks','assigned_to','audio_record'
    )
    change_list_template = "admin/candidate_changelist.html"  # Custom template for extra button (optional)

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload-excel/', self.admin_site.admin_view(self.upload_excel), name='candidate_upload_excel'),
        ]
        return custom_urls + urls

    def upload_excel(self, request):
        if not request.user.is_superuser:
            self.message_user(request, "Only superusers can upload Excel files.", level=messages.ERROR)
            return redirect('..')

        if request.method == "POST":
            form = ExcelUploadForm(request.POST, request.FILES)
            if form.is_valid():
                excel_file = form.cleaned_data['excel_file']

                try:
                    df = pd.read_excel(excel_file)
                except Exception as e:
                    self.message_user(request, f"Error reading Excel file: {e}", level=messages.ERROR)
                    return redirect('..')

                count = 0

                def clean_row(row):
                    return {key: (None if pd.isna(value) else str(value).strip() if isinstance(value, str) else value)
                            for key, value in row.items()}

                for _, row in df.iterrows():
                    cleaned_data = clean_row(row)
                    phone = cleaned_data.get('phone')
                    if not phone:
                        continue

                    assigned_username = cleaned_data.get('assigned_to')
                    assigned_user = None
                    if assigned_username:
                        assigned_user = User.objects.filter(username=assigned_username).first()

                    Candidate.objects.update_or_create(
                        phone=phone,
                        defaults={
                            'first_name': cleaned_data.get('first_name'),
                            'last_name': cleaned_data.get('last_name'),
                            'email': cleaned_data.get('email'),
                            'address': cleaned_data.get('address'),
                            'age': cleaned_data.get('age'),
                            'qualification': cleaned_data.get('qualification'),
                            'interested_area': cleaned_data.get('interested_area'),
                            'current_role': cleaned_data.get('current_role'),
                            'status': cleaned_data.get('status') or 'interested',
                            'remarks': cleaned_data.get('remarks'),
                            'requirements_of_candidate': cleaned_data.get('requirements_of_candidate'),
                            'assigned_to': assigned_user,
                        }
                    )

                    count += 1

                self.message_user(request, f"Successfully imported {count} candidates.")
                return redirect('..')

        else:
            form = ExcelUploadForm()

        context = {
            'form': form,
            'title': 'Upload Excel file for Candidates',
            'opts': self.model._meta,
        }
        return render(request, 'admin/upload_excel.html', context)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff', 'is_superuser', 'is_active')
    search_fields = ('username', 'email')

admin.site.register(User, CustomUserAdmin)



