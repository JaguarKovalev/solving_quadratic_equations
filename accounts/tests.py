from django.test import TestCase
from django.urls import reverse
from accounts.models import CustomUser

class AccountsTests(TestCase):
    def test_user_registration(self):
        response = self.client.post(reverse('register'), {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'strongpassword',
            'password2': 'strongpassword',
        })
        self.assertEqual(response.status_code, 302)  # Ожидаем перенаправление
        self.assertTrue(CustomUser.objects.filter(username='testuser').exists())
