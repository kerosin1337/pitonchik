from django.test import TestCase, RequestFactory, Client
from django.contrib.auth import authenticate, logout
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import *
from .utils import recalc_cart


class UserTest(TestCase):

    def setUp(self) -> None:
        self.user = UserData.objects.create_user(username='eugene', password='5338')

    def test_correct(self):
        user = self.client.login(username='eugene', password='5338')
        self.assertTrue(user)

    def test_wrong_username(self):
        user = self.client.login(username='wrong', password='5338')
        self.assertFalse(user)

    def test_wrong_pssword(self):
        user = self.client.login(username='eugene', password='wrong')
        self.assertFalse(user)

    def test_logout(self):
        user = self.client.login(username='eugene', password='5338')
        session_id = self.client.session['_auth_user_id']
        self.client.logout()
        self.assertNotIn(session_id, self.client.session)

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
        self.cart = Cart.objects.create(owner=self.user)

    def test_category_in_product(self):
        self.assertEqual(self.category, self.product.category)

    def test_cart_product(self):
        self.cart_product = CartProduct.objects.create(
            user=self.user,
            cart=self.cart,
            price=self.product.price,
            product=self.product,
            qty=2
        )
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)
        summ = 0
        for i in self.cart.products.all():
            summ += i.final_price
        self.assertEqual(self.cart.final_price, summ)