import uuid

from django.contrib.auth import authenticate
from django.db import IntegrityError, transaction
from django.test import TestCase
from django.urls import reverse

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import User


class UserModelTests(TestCase):

    def test_create_user(self):
        user = User.objects.create_user(
            email="owner@example.com",
            password="HostelHubTest@123",
        )

        self.assertEqual(user.email, "owner@example.com")
        self.assertTrue(user.check_password("HostelHubTest@123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        self.assertFalse(user.is_email_verified)

    def test_email_normalization(self):
        user = User.objects.create_user(
            email="  Owner@EXAMPLE.COM  ",
            password="HostelHubTest@123",
        )

        user.refresh_from_db()

        self.assertEqual(user.email, "owner@example.com")

    def test_user_id_is_uuid(self):
        user = User.objects.create_user(
            email="owner@example.com",
        )

        self.assertIsInstance(user.id, uuid.UUID)

    def test_empty_email_rejected(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="")

    def test_none_email_rejected(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email=None)

    def test_whitespace_email_rejected(self):
        with self.assertRaises(ValueError):
            User.objects.create_user(email="   ")

    def test_password_is_hashed(self):
        password = "HostelHubTest@123"

        user = User.objects.create_user(
            email="owner@example.com",
            password=password,
        )

        user.refresh_from_db()

        self.assertNotEqual(user.password, password)
        self.assertTrue(user.check_password(password))

    def test_incorrect_password_rejected(self):
        user = User.objects.create_user(
            email="owner@example.com",
            password="HostelHubTest@123",
        )

        self.assertFalse(
            user.check_password("WrongPassword@123")
        )

    def test_user_without_password(self):
        user = User.objects.create_user(
            email="owner@example.com",
        )

        self.assertFalse(user.has_usable_password())

class SuperuserTests(TestCase):

    def test_create_superuser(self):
        user = User.objects.create_superuser(
            email="admin@example.com",
            password="HostelHubTest@123",
        )

        user.refresh_from_db()

        self.assertEqual(user.email, "admin@example.com")
        self.assertTrue(user.is_staff)
        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_active)
        self.assertTrue(user.check_password("HostelHubTest@123"))

    def test_superuser_requires_staff_status(self):
        with self.assertRaisesMessage(
            ValueError,
            "Superuser must have is_staff=True",
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="HostelHubTest@123",
                is_staff=False,
            )

    def test_superuser_requires_superuser_status(self):
        with self.assertRaisesMessage(
            ValueError,
            "Superuser must have is_superuser=True",
        ):
            User.objects.create_superuser(
                email="admin@example.com",
                password="HostelHubTest@123",
                is_superuser=False,
            )

class UserDatabaseConstraintTests(TestCase):

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            email="owner@example.com",
        )

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                User.objects.create_user(
                    email="owner@example.com",
                )

        self.assertEqual(User.objects.count(), 1)

    def test_case_insensitive_duplicate_email_rejected(self):
        User.objects.create_user(
            email="owner@example.com",
        )

        duplicate_user = User(
            email="OWNER@EXAMPLE.COM",
        )
        duplicate_user.set_unusable_password()

        with self.assertRaises(IntegrityError):
            with transaction.atomic():
                duplicate_user.save()

        self.assertEqual(User.objects.count(), 1)

class AuthenticationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.password = "HostelHubTest@123"

        cls.user = User.objects.create_user(
            email="owner@example.com",
            password=cls.password,
        )

    def test_authenticate_with_correct_credentials(self):
        user = authenticate(
            email="owner@example.com",
            password=self.password,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_with_uppercase_email(self):
        user = authenticate(
            email="OWNER@EXAMPLE.COM",
            password=self.password,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_with_mixed_case_email(self):
        user = authenticate(
            email="Owner@Example.Com",
            password=self.password,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_with_whitespace_email(self):
        user = authenticate(
            email="  owner@example.com  ",
            password=self.password,
        )

        self.assertEqual(user, self.user)

    def test_authenticate_with_wrong_password(self):
        user = authenticate(
            email="owner@example.com",
            password="WrongPassword@123",
        )

        self.assertIsNone(user)

    def test_authenticate_with_nonexistent_email(self):
        user = authenticate(
            email="unknown@example.com",
            password=self.password,
        )

        self.assertIsNone(user)

    def test_inactive_user_cannot_authenticate(self):
        self.user.is_active = False
        self.user.save(update_fields=["is_active"])

        user = authenticate(
            email="owner@example.com",
            password=self.password,
        )

        self.assertIsNone(user)

class AdminAuthorizationTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.normal_user = User.objects.create_user(
            email="owner@example.com",
            password="HostelHubTest@123",
        )

        cls.admin_user = User.objects.create_superuser(
            email="admin@example.com",
            password="HostelHubTest@123",
        )

    def test_normal_user_cannot_access_admin(self):
        self.client.force_login(self.normal_user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(
            response,
            reverse("admin:login") + "?next=/admin/",
        )

    def test_superuser_can_access_admin(self):
        self.client.force_login(self.admin_user)

        response = self.client.get(reverse("admin:index"))

        self.assertEqual(response.status_code, 200)

class UserCreationFormTests(TestCase):

    def setUp(self):
        self.form_data = {
            "email": "owner@example.com",
            "password1": "HostelHubTest@123",
            "password2": "HostelHubTest@123",
        }

    def test_valid_creation_form(self):
        form = CustomUserCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()

        self.assertEqual(user.email, "owner@example.com")
        self.assertTrue(user.check_password("HostelHubTest@123"))
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_creation_form_normalizes_email(self):
        self.form_data["email"] = "  Owner@EXAMPLE.COM  "

        form = CustomUserCreationForm(data=self.form_data)

        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()
        user.refresh_from_db()

        self.assertEqual(user.email, "owner@example.com")

    def test_duplicate_email_rejected(self):
        User.objects.create_user(
            email="owner@example.com",
        )

        form = CustomUserCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_uppercase_duplicate_email_rejected(self):
        User.objects.create_user(
            email="owner@example.com",
        )

        self.form_data["email"] = "OWNER@EXAMPLE.COM"

        form = CustomUserCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

    def test_password_mismatch_rejected(self):
        self.form_data["password2"] = "DifferentPassword@123"

        form = CustomUserCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

    def test_weak_password_rejected(self):
        self.form_data["password1"] = "123"
        self.form_data["password2"] = "123"

        form = CustomUserCreationForm(data=self.form_data)

        self.assertFalse(form.is_valid())
        self.assertIn("password2", form.errors)

class UserChangeFormTests(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            email="owner@example.com",
            password="HostelHubTest@123",
        )

        cls.other_user = User.objects.create_user(
            email="manager@example.com",
        )

    def get_form_data(self, email):
        return {
            "email": email,
            "first_name": "Updated",
            "last_name": "Owner",
            "is_active": True,
            "date_joined": self.user.date_joined,
        }

    def test_update_existing_user(self):
        form = CustomUserChangeForm(
            data=self.get_form_data("OWNER@EXAMPLE.COM"),
            instance=self.user,
        )

        self.assertTrue(form.is_valid(), form.errors)

        user = form.save()
        user.refresh_from_db()

        self.assertEqual(user.id, self.user.id)
        self.assertEqual(user.email, "owner@example.com")
        self.assertEqual(user.first_name, "Updated")
        self.assertEqual(user.last_name, "Owner")
        self.assertTrue(user.check_password("HostelHubTest@123"))
        self.assertEqual(User.objects.count(), 2)

    def test_update_with_duplicate_email_rejected(self):
        form = CustomUserChangeForm(
            data=self.get_form_data("MANAGER@EXAMPLE.COM"),
            instance=self.user,
        )

        self.assertFalse(form.is_valid())
        self.assertIn("email", form.errors)

        self.user.refresh_from_db()

        self.assertEqual(self.user.email, "owner@example.com")
