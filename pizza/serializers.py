from rest_framework.serializers import ModelSerializer

from .models import *


class productSerializer(ModelSerializer):

    class Meta:
        model = Products
        fields = '__all__'


class contentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class cartProductsSerializer(ModelSerializer):
    product = productSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = (
            'user',
            'size',
            'price',
            'product',
            'qty',
            'final_price',
        )


class cartSerializer(ModelSerializer):
    products = cartProductsSerializer(read_only=True, many=True)

    class Meta:
        model = Cart
        fields = (
            'owner',
            'products',
            'total_products',
            'final_price',
            'in_order',
            'for_anonymous_user',
            'date_create',
            'qty',
            'is_coupon_activate'
        )


class orderSerializer(ModelSerializer):
    cart = cartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'customer',
            'phone',
            'cart',
            'address',
            'entrance',
            'floor_number',
            'apartment_number',
            'status',
            'buying_type',
            'comment'
        )


class userReal(ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class userSerializer(ModelSerializer):
    user = userReal(read_only=True)

    class Meta:
        model = UserData
        fields = '__all__'
