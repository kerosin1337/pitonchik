from rest_framework.serializers import ModelSerializer

from .models import Products, CartProduct, Cart, UserData, Order, Coupon


class productSerializer(ModelSerializer):
    class Meta:
        model = Products
        fields = '__all__'


class cartProductsSerializer(ModelSerializer):
    product = productSerializer(read_only=True)

    class Meta:
        model = CartProduct
        fields = (
            'id',
            'user',
            'size',
            'price',
            'product',
            'qty',
            'final_price',
        )


class couponSerializer(ModelSerializer):
    class Meta:
        model = Coupon
        fields = '__all__'


class cartSerializer(ModelSerializer):
    products = cartProductsSerializer(read_only=True, many=True)
    coupon = couponSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = (
            'id',
            'owner',
            'products',
            'total_products',
            'final_price',
            'in_order',
            'for_anonymous_user',
            'date_create',
            'qty',
            'coupon'
        )


class orderSerializer(ModelSerializer):
    cart = cartSerializer(read_only=True)

    class Meta:
        model = Order
        fields = (
            'id',
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


# class userReal(ModelSerializer):
#     class Meta:
#         model = User
#         fields = '__all__'


class userSerializer(ModelSerializer):
    # user = userReal(read_only=True)

    class Meta:
        model = UserData
        fields = '__all__'
