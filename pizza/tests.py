from django.test import TestCase
from .models import *
from faker import Faker

fake = Faker()


class ProductsTest(TestCase):
    category = fake.name()
    name = fake.name()
    description = fake.text()
    price = fake.pydecimal()
    image = fake.file_name('image')
    slug = fake.slug()
    def setUp(self):
        category = Category.objects.create(name=self.category)
        Products.objects.create(category=category, name=self.name, description=self.description,
                                price=123,
                                image=self.image, slug=self.slug)

    def test_product_equal(self):
        prod = Products.objects.get(name=self.name, description=self.description)
        self.assertEqual(prod.name, self.name)
