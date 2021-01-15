from django.contrib.auth import get_user_model
from django.test import TestCase


class TestUserProfile(TestCase):

    def test_user_creation(self):
        """
        Testing the creation of a profile for a registered user
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