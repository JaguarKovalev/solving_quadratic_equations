from django.test import TestCase
from django.urls import reverse
from .models import CustomUser

class AccountsTests(TestCase):
    def setUp(self):
        self.user = CustomUser.objects.create_user(username='testuser', email='testuser@example.com', password='password123')

    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'password123',
            'password2': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        self.assertEqual(CustomUser.objects.count(), 2)

    def test_user_login(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'password123'})
        self.assertEqual(response.status_code, 302)  # Redirect after login
        self.assertTrue(response.wsgi_request.user.is_authenticated)

    def test_user_logout(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout
        self.assertFalse('_auth_user_id' in self.client.session)

    def test_password_change(self):
        self.client.login(username='testuser', password='password123')
        response
