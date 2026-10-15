"""
apps/users/tests.py: Kullanıcı ve Kimlik Doğrulama Test Paketi (7 Test)
=======================================================================
Bu dosya, kullanıcı kayıt, JWT giriş ve profil yönetimi işlevlerini izole test veritabanında test eder.

Çalıştırılan Testler:
1. test_kullanici_basariyla_kayit_olabilir         : Geçerli bilgilerle 201 Created döner ve veritabanına kaydeder.
2. test_uyusmayan_sifreyle_kayit_olunamaz          : Parola ve doğrulama uyuşmadığında 400 Bad Request verir.
3. test_ayni_eposta_ile_ikinci_kez_kayit_olunamaz : Mükerrer e-postayla kaydı engeller (400 Bad Request).
4. test_dogru_bilgilerle_jwt_girisi                : Başarılı girişte access ve refresh token döndüğünü doğrular.
5. test_yanlis_sifre_ile_giris_engellenir          : Hatalı şifrede 401 Unauthorized döner.
6. test_giris_yapmayan_profiline_erisemez          : Token göndermeyen anonim isteğe 401 döner.
7. test_giris_yapan_profilini_gorur_ve_gunceller   : JWT ile kendi profilini okuma ve PATCH ile güncelleme testi.
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
