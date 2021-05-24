from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse

User = get_user_model()


def validate_image(image):
    file_size = image.file.size
    limit_mb = 2
    if file_size > limit_mb * 1024 * 1024:
        raise ValidationError("Максимальный размер файла %s MB" % limit_mb)
    # file_size = image.file.size
    # limit_kb = 150
    # if file_size > limit_kb * 1024:
    #     raise ValidationError("Max size of file is %s KB" % limit)


class UserData(models.Model):
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, null=True)
    session = models.CharField(max_length=128, null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name='Номер телефона', null=True, blank=True)
    # address = models.CharField(max_length=255, verbose_name='Адрес', null=True, blank=True)
    #  #                                 blank=True)
    # distance = models.FloatField(verbose_name='Расстояние', null=True, blank=True)
    orders = models.ManyToManyField('Order', verbose_name='Заказы покупателя', related_name='related_order')

    def __str__(self):
        return "Покупатель: {}".format(self.user)


# class LatestProductsManager:
#
#     @staticmethod
#     def get_products_for_main_page(*args, **kwargs):
#         with_respect_to = kwargs.get('with_respect_to')
#         products = []
#         ct_models = ContentType.objects.filter(model__in=args)
#         for ct_model in ct_models:
#             model_products = ct_model.model_class()._base_manager.all().order_by('-id')[:5]
#             products.extend(model_products)
#         if with_respect_to:
#             ct_model = ContentType.objects.filter(model=with_respect_to)
#             if ct_model.exists():
#                 if with_respect_to in args:
#                     return sorted(
#                         products, key=lambda x: x.__class__._meta.model_name.startswith(with_respect_to), reverse=True
#                     )
#         return products


# class LatestProducts:
#     objects = LatestProductsManager()
#
#
# class CategoryManager(models.Manager):
#     CATEGORY_NAME_COUNT_NAME = {
#         'Продукты': 'product__count',
#     }
#
#     def get_queryset(self):
#         return super().get_queryset()
#
#     def get_categories_for_left_sidebar(self):
#         models = get_models_for_count('Products')
#         qs = list(self.get_queryset().annotate(*models))
#         data = [
#             dict(name=c.name, url=c.get_absolute_url(), count=getattr(c, self.CATEGORY_NAME_COUNT_NAME[c.name]))
#             for c in qs
#         ]
#         return data

# class TypeProduct(models.Model):
#     types = models.CharField(max_length=30)
#     slug = models.SlugField(unique=True)
#     objects = CategoryManager()
#
#     def __str__(self):
# return self.types
# PIZZA = 'pizza'
# SNACKS = 'snacks'
# DRINK = 'drink'
# CATEGORY_CHOICES = (
#     (PIZZA, 'Пицца'),
#     (SNACKS, 'Закуски'),
#     (DRINK, 'Напитки'),
# )
# category = models.CharField(
#     max_length=100,
#     verbose_name='Категория',
#     choices=CATEGORY_CHOICES,
# )

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Имя категории')

    def __str__(self):
        return self.name


class Products(models.Model):
    CATEGORY_CHOICES = (
        ('Пицца', 'Пицца'),
        ('Закуски', 'Закуски'),
        ('Напитки', 'Напитки'),
    )
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    # category = models.ForeignKey(Category, verbose_name='category', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=128)
    price = models.DecimalField(max_digits=4, decimal_places=0, default=299)
    price2 = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    price3 = models.DecimalField(max_digits=4, decimal_places=0, null=True)
    image = models.ImageField(upload_to='products',
                              validators=[FileExtensionValidator(allowed_extensions=['png']), validate_image])
    slug = models.SlugField(unique=True)
    is_custom = models.BooleanField(null=True, blank=True, default=False)

    def __str__(self):
        return self.name

    def get_model_name(self):
        return self.__class__.__name__.lower()


class CartProduct(models.Model):
    user = models.ForeignKey('UserData', verbose_name='Покупатель', on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey('Cart', verbose_name='Корзина', on_delete=models.CASCADE, related_name='related_products')
    size = models.CharField(max_length=20)
    price = models.DecimalField(max_digits=4, decimal_places=0)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    # content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    # object_id = models.PositiveIntegerField()
    # content_object = GenericForeignKey('content_type', 'object_id')
    qty = models.PositiveIntegerField(default=1)
    final_price = models.DecimalField(max_digits=9, decimal_places=2, verbose_name='Общая цена')

    def __str__(self):
        return "Продукт: {} (для корзины)".format(self.product.name)

    def save(self, *args, **kwargs):
        self.final_price = self.qty * self.price
        super().save(*args, **kwargs)


class Cart(models.Model):
    owner = models.ForeignKey('UserData', null=True, verbose_name='Владелец', on_delete=models.CASCADE)
    products = models.ManyToManyField(CartProduct, blank=True, related_name='related_cart')
    total_products = models.PositiveIntegerField(default=0)
    final_price = models.DecimalField(max_digits=9, default=0, decimal_places=2, verbose_name='Общая цена')
    in_order = models.BooleanField(default=False)
    for_anonymous_user = models.BooleanField(default=False)
    date_create = models.DateTimeField(auto_now_add=True)
    qty = models.PositiveIntegerField(default=0)
    coupon = models.ForeignKey('Coupon', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return str(self.id)


class Order(models.Model):
    STATUS_NEW = 'new'
    STATUS_IN_PROGRESS = 'in_progress'
    STATUS_READY = 'is_ready'
    STATUS_COMPLETED = 'completed'

    BUYING_TYPE_SELF = 'self'
    BUYING_TYPE_DELIVERY = 'delivery'

    STATUS_CHOICES = (
        (STATUS_NEW, 'Новый заказ'),
        (STATUS_IN_PROGRESS, 'Заказ в обработке'),
        (STATUS_READY, 'Заказ готов'),
        (STATUS_COMPLETED, 'Заказ выполнен')
    )

    BUYING_TYPE_CHOICES = (
        (BUYING_TYPE_SELF, 'Самовывоз'),
        (BUYING_TYPE_DELIVERY, 'Доставка')
    )

    customer = models.ForeignKey(UserData, verbose_name='Покупатель', related_name='related_orders',
                                 on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, verbose_name='Телефон')
    cart = models.ForeignKey(Cart, verbose_name='Корзина', on_delete=models.CASCADE, null=True, blank=True)
    address = models.CharField(max_length=128, verbose_name='Адрес', null=True, blank=True)
    entrance = models.CharField(max_length=128, verbose_name='Подъезд', null=True, blank=True)
    floor_number = models.CharField(max_length=128, verbose_name='Этаж', null=True, blank=True)
    apartment_number = models.CharField(max_length=128, verbose_name='Квартира', null=True, blank=True)
    status = models.CharField(
        max_length=100,
        verbose_name='Статус заказ',
        choices=STATUS_CHOICES,
        default=STATUS_NEW
    )
    buying_type = models.CharField(
        max_length=100,
        verbose_name='Тип заказа',
        choices=BUYING_TYPE_CHOICES,
        default=BUYING_TYPE_SELF
    )
    comment = models.TextField(verbose_name='Комментарий к заказу', null=True, blank=True)
    created_at = models.DateTimeField(auto_now=True, verbose_name='Дата создания заказа')

    def __str__(self):
        return str(self.id)


class Coupon(models.Model):
    code = models.CharField(max_length=15, verbose_name='Купон', unique=True)
    sale = models.IntegerField(verbose_name='Скидка', validators=[MinValueValidator(1), MaxValueValidator(100)])

    # users = models.ManyToManyField(UserData, blank=True, null=True, related_name='related_coupon')

    def __str__(self):
        return '{}, {}%'.format(self.code, self.sale)
