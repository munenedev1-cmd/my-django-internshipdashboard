from django.conf import settings
from django.db import models


class InternshipApplication(models.Model):
    STATUS_CHOICES = [
        ("draft", "Draft"),
        ("submitted", "Submitted"),
        ("under_review", "Under Review"),
        ("shortlisted", "Shortlisted"),
        ("rejected", "Rejected"),
    ]

    YES_NO_CHOICES = [
        ("YES", "YES"),
        ("NO", "NO"),
    ]

    GENDER_CHOICES = [
        ("MALE", "MALE"),
        ("FEMALE", "FEMALE"),
    ]

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="internship_application")

    email = models.EmailField()
    full_name = models.CharField(max_length=200)
    national_id_number = models.CharField(max_length=30)
    birth_certificate_entry_number = models.CharField(max_length=100)
    kra_pin_number = models.CharField(max_length=30)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    disability = models.CharField(max_length=10, choices=YES_NO_CHOICES)
    date_of_birth = models.DateField()
    mobile_number = models.CharField(max_length=30)
    next_of_kin_name = models.CharField(max_length=200)
    next_of_kin_mobile = models.CharField(max_length=30)
    county_of_birth = models.CharField(max_length=100)
    sub_county = models.CharField(max_length=100)
    village = models.CharField(max_length=100)
    ethnicity = models.CharField(max_length=100)
    level_of_training = models.CharField(max_length=50)
    institution = models.CharField(max_length=200)
    year_of_graduation = models.IntegerField()
    kvb_intern_number = models.CharField(max_length=100)
    internship_preference = models.CharField(max_length=200)
    bank_name = models.CharField(max_length=200)
    bank_branch = models.CharField(max_length=200)
    bank_account_number = models.CharField(max_length=50)
    account_name = models.CharField(max_length=200)
    civil_servant = models.CharField(max_length=10, choices=YES_NO_CHOICES)
    government_personal_number = models.CharField(max_length=50, blank=True, default="")
    shif_membership_number = models.CharField(max_length=100, blank=True, default="")
    nssf_membership_number = models.CharField(max_length=100, blank=True, default="")

    national_id_document = models.FileField(upload_to="documents/id/")
    birth_certificate_document = models.FileField(upload_to="documents/birth/")
    passport_photo = models.FileField(upload_to="documents/photo/")
    kra_pin_certificate = models.FileField(upload_to="documents/kra/")

    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default="submitted")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name
