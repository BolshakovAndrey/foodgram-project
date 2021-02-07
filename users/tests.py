from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import resolve, reverse

from .forms import UserCreationForm
from .views import SignUp


class TestUserProfile(TestCase):

    def test_user_creation(self):
        """
        Тестирование создания профиля для зарегистрированного пользователя/суперпользователя
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
    """
    Тестирование страницы регистрации
    """

    def setUp(self):
        url = reverse('signup')
        self.response = self.client.get(url)

    def test_signup_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'registration/signup.html')
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
