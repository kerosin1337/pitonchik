import json

import stripe
from django.contrib.auth.views import *
from django.shortcuts import render
from django.views.generic import *
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from .consumers import OrderWS
from .forms import *
from .mixins import *
from .serializers import *
from .utils import *


# class user(ModelViewSet):
#     queryset = User.objects.order_by()
#     serializer_class = userReal
#     model = User

class userAPI(ModelViewSet):
    serializer_class = userSerializer
    model = UserData

    def get_queryset(self):
        return UserData.objects.filter(user=self.request.user.id)


class productsAPI(ModelViewSet):
    queryset = Products.objects.filter(is_custom=False)
    serializer_class = productSerializer


class cartProductsAPI(ModelViewSet):
    serializer_class = cartProductsSerializer
    model = CartProduct

    def get_queryset(self):
        return CartProduct.objects.filter(user=self.request.user.id)


class cartAPI(ReadOnlyModelViewSet):
    serializer_class = cartSerializer
    model = Cart

    def get_queryset(self):
        return Cart.objects.filter(owner=self.request.user.id, in_order=False)


class index(TemplateView):
    template_name = 'main.html'


class login(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_redirect_url())
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_redirect_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return '/admin'
        else:
            return '/'


class register(CreateView):
    template_name = 'register.html'
    model = UserData
    form_class = RegForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('register'))


# LoginRequiredMixin
class LogoutView(LogoutView):
    template_name = 'logout.html'


class Profile(CartMixin, View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        user, created = UserData.objects.get_or_create(user=self.cart.owner_id)
        if created:
            user = UserData.objects.get(user=self.cart.owner_id)
        # social = SocialAccount.objects.get(user=request.user) or None
        context = {
            'user': user,
            # 'img': social.extra_data['picture']
        }
        return render(request, 'profile.html', context)


class AddToCartView(CartMixin, View):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        product_slug = kwargs.get('slug')
        try:
            custom = body['custom']
        except:
            custom = None
        if custom:
            Products.objects.get_or_create(name='Моя пицца', description=body['description'], price=body['price'],
                                           image='products/custom.png', slug=product_slug, is_custom=True)
        product = Products.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart,
            size=body['size'], price=body['price'], product=product
        )
        if created:
            self.cart.products.add(cart_product)
        else:
            q = CartProduct.objects.get(
                user=self.cart.owner, cart=self.cart,
                size=body['size'], price=body['price'], product=product
            )
            q.qty += 1
            q.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect(reverse('index'))


class DeleteFromCartView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        product_slug = kwargs.get('slug')
        # content_type = ContentType.objects.get(model=ct_model)
        product = Products.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
            size=body['size']
        )
        self.cart.products.remove(cart_product)
        cart_product.delete()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/basket/')


class ChangeQTYView(CartMixin, View):

    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        product_slug = kwargs.get('slug')
        # content_type = ContentType.objects.get(model=ct_model)
        product = Products.objects.get(slug=product_slug)
        cart_product = CartProduct.objects.get(
            user=self.cart.owner, cart=self.cart, product=product,
            size=body['size']
        )
        qty = body['qty']
        cart_product.qty = qty
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/basket/')


def deleteCart(request):
    Cart.objects.filter(owner=request.user.id).delete()
    return HttpResponseRedirect(reverse('basket'))


class basket(CartMixin, View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'basket.html', context)


class order(CartMixin, View):
    def get(self, request, *args, **kwargs):
        try:
            stripe.api_key = 'sk_test_51IgOVCHac5lTiSCzjs3ZKXz3C9o6WtQ0w03byY1RGR0fbrVbt0vOAcePoe7AfXPKYlIE9OJAsr2thd6cf3s8hBkE00LLZ5Sn4N'
            intent = stripe.PaymentIntent.create(
                amount=int(self.cart.final_price * 100),
                currency='rub',
                metadata={'integration_check': 'accept_a_payment'}
            )
            try:
                order = Order.objects.get(customer=self.cart.owner, cart=self.cart)
            except:
                order = None
            context = {
                'order': order,
                'cart': self.cart,
                'client_secret': intent.client_secret
            }
            return render(request, 'order.html', context)
        except:
            return HttpResponseRedirect(reverse('index'))


# try:
#     if request.user.is_authenticated:
#         cart = Cart.objects.filter(owner=request.user.id, in_order=False).first()
#     else:
#         cart = Cart.objects.filter(for_anonymous_user=True, in_order=False).first()
#     stripe.api_key = 'sk_test_51IgOVCHac5lTiSCzjs3ZKXz3C9o6WtQ0w03byY1RGR0fbrVbt0vOAcePoe7AfXPKYlIE9OJAsr2thd6cf3s8hBkE00LLZ5Sn4N'
#     intent = stripe.PaymentIntent.create(
#         amount=int(cart.final_price * 100),
#         currency='rub',
#         metadata={'integration_check': 'accept_a_payment'}
#     )
#     context = {
#         'order': Order.objects.get(cart=cart),
#         'cart': cart,
#         'client_secret': intent.client_secret
#     }
#     return render(request, 'order.html', context)
# except AttributeError:
#     return HttpResponseRedirect(reverse('index'))


class OrderAccept(CartMixin, View):
    def post(self, request, *args, **kwargs):
        # requests.post('ws://localhost:8000/order/', json={'qwe': 123})
        req = request.POST
        order, created = Order.objects.get_or_create(
            customer=self.cart.owner,
            phone=req['tel'], cart=self.cart, buying_type=req['buying_type'],
            address=req['address'] or None, entrance=req['entrance'] or None,
            floor_number=req['floor_number'] or None,
            apartment_number=req['apartment_number'] or None, comment=req['comment'] or None
        )
        if created and self.cart.owner is not None:
            self.cart.owner.orders.add(order)
        return HttpResponseRedirect(reverse('order'))

    def get(self, request, *args, **kwargs):
        try:
            self.post(self, request, *args, **kwargs)
        except AttributeError:
            return HttpResponseRedirect(reverse('index'))


class OrderPayment(CartMixin, View):
    def post(self, request, *args, **kwargs):
        # for i in self.cart.products.all().filter(product__is_custom=True):
        #     i.product.delete()
        self.cart.in_order = True
        self.cart.save()
        order = Order.objects.get(customer=self.cart.owner_id, cart=self.cart)
        order.status = 'in_progress'
        order.save()
        return HttpResponseRedirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        if not self.cart.products.all():
            return HttpResponseRedirect(reverse('index'))


class Custom(TemplateView):
    template_name = 'custom.html'


def room(request, room_name):
    return render(request, 'staffOrder.html', {
        'room_name': room_name
    })
