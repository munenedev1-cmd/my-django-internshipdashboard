from django.contrib import admin

from .models import InternshipApplication


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    list_display = ["full_name", "status", "institution", "created_at"]
    list_filter = ["status", "gender", "civil_servant"]
    search_fields = ["full_name", "national_id_number", "email"]
