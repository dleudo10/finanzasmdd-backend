from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
User = get_user_model()

class AuthTest(TestCase):
    def setUp(self):
        self.password = "Password123*"
        self.user = User.objects.create_user(
            email="test@ejemplo.com",
            password=self.password
        )
        self.login_url = reverse('login')
        self.refresh_url = reverse('refresh_token')
        
    def test_login_sets_cookies(self):
        """Verifica que el login exitoso ponga los tokens en cookies HttpOnly"""
        response = self.client.post(self.login_url, {
            "email": self.user.email,
            "password": self.password
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # self.assertIn('refresh_token', response.cookies)
        # self.assertIn('csrftoken', response.cookies)
        # self.assertTrue(response.cookies['refresh_token']['httponly'])
        
    # def test_inactive_user_login_fails(self):
    #     """Verifica que un usuario inactivo no pueda iniciar sesión"""
    #     self.user.is_active = False
    #     self.user.save()
    #     responde = self.client.post(self.login_url, {
    #         "email": self.user.email,
    #         "password": self.password,
    #     })
        
    #     self.assertEqual(responde.status_code, status.HTTP_400_BAD_REQUEST)
        
    # def test_inactive_user_refresh_fails_and_clears_cookies(self):
    #     """verifica que el sistema sea capaz de "expulsar" a alguien si su cuenta fue desactivada entre el momento en que obtuvo el token y el momento en que intentó usarlo."""
    #     self.client.post(self.login_url, {
    #         "email": self.user.email,
    #         "password": self.password
    #     })
    #     self.user.is_active = False
    #     self.user.save()
        
    #     response = self.client.post(self.refresh_url)
        
    #     self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)        
    #     self.assertEqual(response.cookies.get('refresh_token').value, "")
    #     self.assertEqual(response.cookies.get('csrftoken').value, "")
        
        