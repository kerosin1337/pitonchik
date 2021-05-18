from django.test import TestCase
from .models import Products
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
        Products.objects.create(category=self.category, name=self.name, description=self.description,
                                price=123,
                                image=self.image, slug=self.slug)

    def test_product_equal(self):
        prod = Products.objects.get(category=self.category)
        self.assertEqual(prod.category, self.category)
