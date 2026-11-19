from datetime import date
from pathlib import Path
import shutil
import tempfile

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase, override_settings
from django.urls import reverse

from .models import InternshipApplication, validate_document, validate_photo

TEST_PDF_CONTENT = b"%PDF-1.4\n1 0 obj<</Type/Catalog>>endobj\ntrailer<</Root 1 0 R>>\n%%EOF\n"
TEST_MEDIA_ROOT = Path(tempfile.mkdtemp(prefix="internship-portal-test-media-"))


class AccountFlowTests(TestCase):
    def test_registration_creates_account_and_logs_user_in(self):
        response = self.client.post(reverse("register"), {
            "username": "applicant", "email": "applicant@example.com",
            "password1": "StrongPass!7391", "password2": "StrongPass!7391",
        })
        self.assertRedirects(response, reverse("apply"))
        self.assertTrue(get_user_model().objects.filter(username="applicant").exists())
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_dashboard_requires_login(self):
        response = self.client.get(reverse("dashboard"))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('dashboard')}")


@override_settings(MEDIA_ROOT=TEST_MEDIA_ROOT)
class DocumentProtectionTests(TestCase):
    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        shutil.rmtree(TEST_MEDIA_ROOT, ignore_errors=True)

    def setUp(self):
        TEST_MEDIA_ROOT.mkdir(parents=True, exist_ok=True)
        User = get_user_model()
        self.owner = User.objects.create_user(username="owner", password="Pass!7391")
        self.other = User.objects.create_user(username="other", password="Pass!7391")
        self.application = InternshipApplication.objects.create(
            user=self.owner, email="owner@example.com", full_name="Test Applicant",
            national_id_number="12345678", birth_certificate_entry_number="BC123",
            kra_pin_number="A123456789Z", gender="MALE", disability="NO",
            date_of_birth=date(2000, 1, 1), mobile_number="0700000000",
            next_of_kin_name="Relative", next_of_kin_mobile="0711111111",
            county_of_birth="Nairobi", sub_county="Westlands", village="Village",
            ethnicity="Prefer not to say", level_of_training="Degree",
            institution="University", year_of_graduation=2024,
            kvb_intern_number="KVB-1", internship_preference="Nairobi",
            bank_name="Bank", bank_branch="Branch", bank_account_number="12345",
            account_name="Test Applicant", civil_servant="NO",
            national_id_document=SimpleUploadedFile(
                "id.pdf", TEST_PDF_CONTENT, content_type="application/pdf"
            ),
            birth_certificate_document=SimpleUploadedFile(
                "birth.pdf", b"%PDF-1.4\n%%EOF\n", content_type="application/pdf"
            ),
            passport_photo=SimpleUploadedFile(
                "photo.jpg", b"test image bytes", content_type="image/jpeg"
            ),
            kra_pin_certificate=SimpleUploadedFile(
                "kra.pdf", b"%PDF-1.4\n%%EOF\n", content_type="application/pdf"
            ),
        )

    def tearDown(self):
        for field in (
            "national_id_document", "birth_certificate_document",
            "passport_photo", "kra_pin_certificate",
        ):
            getattr(self.application, field).delete(save=False)

    def test_owner_can_download_document(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("application_document", args=[self.application.pk, "national_id_document"])
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(b"".join(response.streaming_content), TEST_PDF_CONTENT)

    def test_other_applicant_cannot_download_document(self):
        self.client.force_login(self.other)
        response = self.client.get(
            reverse("application_document", args=[self.application.pk, "national_id_document"])
        )
        self.assertEqual(response.status_code, 404)

    def test_unauthenticated_user_cannot_download_document(self):
        response = self.client.get(
            reverse("application_document", args=[self.application.pk, "national_id_document"])
        )
        self.assertEqual(response.status_code, 302)

    def test_non_document_fields_are_not_downloadable(self):
        self.client.force_login(self.owner)
        response = self.client.get(
            reverse("application_document", args=[self.application.pk, "bank_account_number"])
        )
        self.assertEqual(response.status_code, 404)


class UploadValidationTests(TestCase):
    def test_documents_reject_unapproved_extension(self):
        with self.assertRaises(ValidationError):
            validate_document(SimpleUploadedFile("script.html", b"<script>"))

    def test_documents_reject_files_over_five_megabytes(self):
        with self.assertRaises(ValidationError):
            validate_document(SimpleUploadedFile("id.pdf", b"x" * (5 * 1024 * 1024 + 1)))

    def test_photo_only_accepts_image_extensions(self):
        with self.assertRaises(ValidationError):
            validate_photo(SimpleUploadedFile("photo.pdf", b"not an image"))
