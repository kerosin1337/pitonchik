from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import authenticate, logout
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import *


class UserTest(TestCase):

    def setUp(self) -> None:
        self.user = UserData.objects.create_user(username='eugene', password='5338')

    def test_correct(self):
        user = authenticate(username='eugene', password='5338')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='12test12')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_pssword(self):
        user = authenticate(username='test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_logout(self):
        self.client = Client()
        self.client.login(username='eugene', password='5338')


    def tearDown(self):
        self.user.delete()


class ProductTest(TestCase):
    def setUp(self) -> None:
        self.user = UserData.objects.create_user(username='eugene', password='5338')
        self.category = Category.objects.create(name='test')
        self.product = Products.objects.create(
            category=self.category,
            name='test',
            description='test',
            image=SimpleUploadedFile('test.png', content_type='image/jpeg', content=''),
        )

    def test_category_in_product(self):
        self.assertEqual(self.category, self.product.category)
