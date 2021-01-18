from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse, resolve

from .forms import UserCreationForm
from .views import SignUp
# from django.contrib.auth.models import User


# class TestIndexView(TestCase):
#     def test_anonymous_cannot_see_page(self):
#         response = self.client.get(reverse("index"))
#         self.assertRedirects(response, "/accounts/login/?next=/index/")
#
#     def test_authenticated_user_can_see_page(self):
#         user = User.objects.create_user("Juliana," "juliana@dev.io", "some_pass")
#         self.client.force_login(user=user)
#         response = self.client.get(reverse("index"))
#         self.assertEqual(response.status_code, 200)

class TestUserProfile(TestCase):

    def test_user_creation(self):
        """
        Testing the creation of a profile for a registered user/superuser
        """
        User = get_user_model()
        user = User.objects.create_user(
            username='test_profile',
            email='testmail@email.com',
            password='password_test'
        )
        self.assertEqual(user.username, 'test_profile')
        self.assertEqual(user.email, 'testmail@email.com')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(
            username='superadmin',
            email='superadmin@email.com',
            password='password_test'
        )
        self.assertEqual(admin_user.username, 'superadmin')
        self.assertEqual(admin_user.email, 'superadmin@email.com')
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)


class SignupPageTests(TestCase):

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'users/signup.html')
        self.assertContains(self.response, 'Регистрация')
        self.assertNotContains(
            self.response, 'I should not be on the page.')

    def test_signup_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, UserCreationForm)
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_signup_view(self):
        view = resolve('/auth/signup/')
        self.assertEqual(
            view.func.__name__,
            SignUp.as_view().__name__
        )
