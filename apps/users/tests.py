"""
apps/users/tests.py: User and Authentication Test Suite (7 Tests)
================================================================
Comprehensive test cases verifying user registration, JWT token generation, and profile security.

Executed Tests:
1. test_kullanici_basariyla_kayit_olabilir         : Verifies 201 Created and user creation upon valid registration.
2. test_uyusmayan_sifreyle_kayit_olunamaz          : Ensures 400 Bad Request when password confirmation mismatches.
3. test_ayni_eposta_ile_ikinci_kez_kayit_olunamaz : Prevents duplicate email registrations with 400 Bad Request.
4. test_dogru_bilgilerle_jwt_girisi                : Validates that valid credentials return both access and refresh tokens.
5. test_yanlis_sifre_ile_giris_engellenir          : Confirms 401 Unauthorized for incorrect passwords.
6. test_giris_yapmayan_profiline_erisemez          : Ensures unauthenticated requests cannot access profile (401).
7. test_giris_yapan_profilini_gorur_ve_gunceller   : Tests profile retrieval and partial update (PATCH) with valid JWT.
"""

from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase

User = get_user_model()


class UserAuthTests(APITestCase):
    """
    Kullanıcı Kayıt, Giriş (JWT) ve Profil Testleri
    """
    def setUp(self):
        self.register_url = '/api/v1/auth/register/'
        self.login_url = '/api/v1/auth/login/'
        self.profile_url = '/api/v1/auth/profile/'

        self.user_data = {
            'email': 'ahmet@test.com',
            'first_name': 'Ahmet',
            'last_name': 'Yılmaz',
            'password': 'Password123!',
            'password_confirm': 'Password123!'
        }
        # Mevcut bir kullanıcı
        self.existing_user = User.objects.create_user(
            email='mevcut@test.com',
            password='Password123!',
            first_name='Mevcut',
            last_name='Kullanici'
        )

    def test_kullanici_basariyla_kayit_olabilir(self):
        response = self.client.post(self.register_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(email='ahmet@test.com').exists())

    def test_uyusmayan_sifreyle_kayit_olunamaz(self):
        data = self.user_data.copy()
        data['password_confirm'] = 'FarkliSifre!'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_ayni_eposta_ile_ikinci_kez_kayit_olunamaz(self):
        data = self.user_data.copy()
        data['email'] = 'mevcut@test.com'
        response = self.client.post(self.register_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dogru_bilgilerle_jwt_girisi(self):
        payload = {
            'email': 'mevcut@test.com',
            'password': 'Password123!'
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)

    def test_yanlis_sifre_ile_giris_engellenir(self):
        payload = {
            'email': 'mevcut@test.com',
            'password': 'YanlisSifre!'
        }
        response = self.client.post(self.login_url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_giris_yapmayan_profiline_erisemez(self):
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_giris_yapan_profilini_gorur_ve_gunceller(self):
        self.client.force_authenticate(user=self.existing_user)
        # 1. Görüntüleme
        get_res = self.client.get(self.profile_url)
        self.assertEqual(get_res.status_code, status.HTTP_200_OK)
        self.assertEqual(get_res.data['email'], 'mevcut@test.com')

        # 2. Güncelleme
        patch_res = self.client.patch(self.profile_url, {'first_name': 'YeniAd'}, format='json')
        self.assertEqual(patch_res.status_code, status.HTTP_200_OK)
        self.existing_user.refresh_from_db()
        self.assertEqual(self.existing_user.first_name, 'YeniAd')
