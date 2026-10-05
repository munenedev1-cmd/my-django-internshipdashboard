from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import InternshipApplication


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user


class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        fields = [
            "email",
            "full_name",
            "national_id_number",
            "birth_certificate_entry_number",
            "kra_pin_number",
            "gender",
            "disability",
            "date_of_birth",
            "mobile_number",
            "next_of_kin_name",
            "next_of_kin_mobile",
            "county_of_birth",
            "sub_county",
            "village",
            "ethnicity",
            "level_of_training",
            "institution",
            "year_of_graduation",
            "kvb_intern_number",
            "internship_preference",
            "bank_name",
            "bank_branch",
            "bank_account_number",
            "account_name",
            "civil_servant",
            "government_personal_number",
            "shif_membership_number",
            "nssf_membership_number",
            "national_id_document",
            "birth_certificate_document",
            "passport_photo",
            "kra_pin_certificate",
        ]
        widgets = {
            "date_of_birth": forms.DateInput(attrs={"type": "date"}),
        }
