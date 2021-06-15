import json
import random
from django.urls import reverse_lazy, reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from faker import Faker

from .models import *
from .utils import recalc_cart

fake = Faker('ru_RU')


class UserTest(TestCase):

    def setUp(self) -> None:
        self.user = UserData.objects.create_user(username='eugene', password='5338', first_name=fake.first_name())

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


class ProductToCartTest(TestCase):
    def summ(self):
        summa = 0
        for i in self.cart.products.all():
            summa += i.final_price
        return summa

    def setUp(self) -> None:
        self.user = UserData.objects.create_user(username='eugene', password='5338')
        self.category = Category.objects.create(name='test')
        self.product = Products.objects.create(
            category=self.category,
            name='test',
            description='test',
            image=SimpleUploadedFile('test.png', content_type='image/jpeg', content=''),
            slug='test-slug'
        )
        self.cart = Cart.objects.create(owner=self.user)
        self.cart_product = CartProduct.objects.create(
            user=self.user,
            cart=self.cart,
            price=self.product.price,
            product=self.product,
            qty=2
        )
        self.cart.products.add(self.cart_product)
        recalc_cart(self.cart)

    def test_category_in_product(self):
        self.assertEqual(self.category, self.product.category)

    def test_cart_product(self):
        self.assertEqual(self.cart.final_price, self.summ())
        self.assertIn(self.cart_product, self.cart.products.all())

    def test_change_qty_cart_product(self):
        randomQTY = random.randint(1, 5)
        self.cart_product.qty = randomQTY
        recalc_cart(self.cart)
        self.assertEqual(self.cart_product.qty, randomQTY)
        self.assertEqual(self.cart.final_price, self.summ())
        self.assertIn(self.cart_product, self.cart.products.all())

    def test_delete_cart_product(self):
        self.cart.products.remove(self.cart_product)
        recalc_cart(self.cart)
        self.assertNotIn(self.cart_product, self.cart.products.all())
        self.assertEqual(self.cart.final_price, self.summ())

    def test_custom(self):
        response = self.client.post(reverse('custom'),
                                    {'slug': 'test', 'description': 'test', 'price': 569, 'size': '25'})
        print(response.context)
    # def test_order(self):
    #     if bool(random.getrandbits(1)):
    #
    #     else:

    # def tearDown(self) -> None:
    #     self.user.delete()
    #     self.product.delete()
    #     self.cart.delete()
