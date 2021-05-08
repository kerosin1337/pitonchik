from rest_framework.serializers import ModelSerializer

from .models import *


class categorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class productSerializer(ModelSerializer):
    # category = categorySerializer(read_only=True)

    class Meta:
        model = Products
        fields = '__all__'


class contentTypeSerializer(ModelSerializer):
    class Meta:
        model = ContentType
        fields = '__all__'


class cartProductsSerializer(ModelSerializer):
    # content_type = contentTypeSerializer(read_only=True)
    product = productSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = (
            'user',
            'size',
            'price',
            # 'content_type',
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
            'qty'
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
