import json

import stripe
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, auth_login, PasswordChangeView
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.contrib import messages
from rest_framework.viewsets import ReadOnlyModelViewSet

from .forms import RegForm
from .mixins import CartMixin
from .models import UserData, Products, CartProduct, Cart, Order, Coupon
from .serializers import userSerializer, productSerializer, cartProductsSerializer, cartSerializer, orderSerializer
from .utils import recalc_cart


# class user(ModelViewSet):
#     queryset = User.objects.order_by()
#     serializer_class = userReal
#     model = User


class userAPI(ReadOnlyModelViewSet):
    serializer_class = userSerializer
    model = UserData

    def get_queryset(self):
        return UserData.objects.filter(id=self.request.user.id)


class productsAPI(ReadOnlyModelViewSet):
    queryset = Products.objects.filter(is_custom=False)
    serializer_class = productSerializer


class cartProductsAPI(ReadOnlyModelViewSet):
    serializer_class = cartProductsSerializer
    model = CartProduct

    def get_queryset(self):
        return CartProduct.objects.filter(user=self.request.user.id)


class cartAPI(ReadOnlyModelViewSet):
    serializer_class = cartSerializer
    model = Cart

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Cart.objects.filter(owner=self.request.user.id, in_order=False)
        else:
            if not self.request.session.session_key:
                self.request.session.save()
            return Cart.objects.filter(session=self.request.session.session_key, in_order=False)


class orderAPI(ReadOnlyModelViewSet):
    serializer_class = orderSerializer
    queryset = Order.objects.order_by()


class index(generic.TemplateView):
    template_name = 'main.html'


class login(LoginView):
    template_name = 'login.html'

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            Cart.objects.filter(session=self.request.session.session_key).delete()
            auth_login(self.request, form.get_user())
            return HttpResponseRedirect(self.get_redirect_url())
        else:
            return HttpResponseRedirect(reverse('login'))

    def get_redirect_url(self):
        if self.request.user.is_superuser or self.request.user.is_staff:
            return '/admin'
        else:
            return '/'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)


class register(generic.CreateView):
    template_name = 'register.html'
    model = UserData
    form_class = RegForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        if self.request.recaptcha_is_valid:
            Cart.objects.filter(session=self.request.session.session_key).delete()
            form.save()
            return HttpResponseRedirect(reverse('login'))
        else:
            return HttpResponseRedirect(reverse('register'))

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('index'))
        return super().get(request, *args, **kwargs)


# class Logout(LogoutView):
#     template_name = 'logout.html'


class Profile(CartMixin, LoginRequiredMixin):
    def get(self, request, *args, **kwargs):
        # user, created = UserData.objects.get_or_create(id=self.cart.owner_id)
        user = UserData.objects.get(id=self.cart.owner_id)
        # social = SocialAccount.objects.get(user=request.user) or None
        context = {
            'user': user,
            # 'img': social.extra_data['picture']
        }

        return render(request, 'profile.html', context)

    def delete(self, request, *args, **kwargs):
        self.cart.owner.delete()
        return HttpResponseRedirect(reverse('index'))


class ChangePasswdView(PasswordChangeView, LoginRequiredMixin):
    template_name = 'ChangePassWD.html'
    success_url = reverse_lazy('user_profile')

    # def post(self, request, *args, **kwargs):
    #     print(123)

class AddToCartView(CartMixin, generic.View):
    def post(self, request, *args, **kwargs):
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        product_slug = kwargs.get('slug')
        try:
            custom = body['custom']
        except:
            custom = None
        if custom:
            product, created = Products.objects.get_or_create(name='Моя пицца', description=body['description'],
                                                              price=body['price'],
                                                              image='products/custom.png', slug=product_slug,
                                                              is_custom=True)
        else:
            product = Products.objects.get(slug=product_slug)
        cart_product, created = CartProduct.objects.get_or_create(
            user=self.cart.owner, cart=self.cart,
            size=request.GET['size'], price=body['price'], product=product
        )
        if created:
            self.cart.products.add(cart_product)
        else:
            q = CartProduct.objects.get(id=cart_product.id)
            q.qty += 1
            q.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect('/')


class DeleteFromCartView(CartMixin, generic.View):

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


class ChangeQTYView(CartMixin, generic.View):

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
        cart_product.qty = body['qty']
        cart_product.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect(reverse('cart'))


class deleteCart(CartMixin):
    # Cart.objects.filter(owner=request.user.id).delete()
    def get(self, request, *args, **kwargs):
        self.cart.delete()
        return HttpResponseRedirect(reverse('basket'))


class basket(CartMixin, generic.View):

    def get(self, request, *args, **kwargs):
        context = {
            'cart': self.cart,
        }
        return render(request, 'basket.html', context)

    def post(self, request, *args, **kwargs):
        coupon = Coupon.objects.all()
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        if self.cart.coupon:
            return JsonResponse({'data': 'Промокод использован.', 'status': 1})
        else:
            for i, obj in enumerate(coupon):
                if obj.code == body['code']:
                    self.cart.coupon = obj
                    self.cart.save()
                    recalc_cart(self.cart)
            return JsonResponse({'data': 'Такого промокода нет.', 'status': 4})

    def delete(self, request, *args, **kwargs):
        self.cart.coupon = None
        self.cart.save()
        recalc_cart(self.cart)
        return HttpResponseRedirect(reverse('index'))
        # if self.cart.is_coupon_activate:
        #     return JsonResponse({'data': 'Вы уже использовали промокод.', 'status': 1})
        # for i, obj in enumerate(coupon):
        #     if obj.code == body['code']:
        #         if len(obj.users.all()) == 0:
        #             self.cart.final_price = int(self.cart.final_price) * (100 - obj.sale) / 100
        #             self.cart.is_coupon_activate = True
        #             obj.users.add(self.cart.owner)
        #             self.cart.save()
        #             return JsonResponse({'data': 'Промокод активирован.', 'status': 2})
        #         # for j in obj.users.all():
        #         #     if j == self.cart.owner:
        #         #         return JsonResponse({'data': 'Вы уже использовали этот промокод'})
        #         for j in obj.users.all():
        #             if j != self.cart.owner:
        #                 self.cart.final_price = int(self.cart.final_price) * (100 - obj.sale) / 100
        #                 self.cart.is_coupon_activate = True
        #                 obj.users.add(self.cart.owner)
        #                 self.cart.save()
        #                 return JsonResponse({'data': 'Промокод активирован.', 'status': 3})
        #         print(list(obj.users.all()).index(request.user))
        #         self.cart.final_price = int(self.cart.final_price) * (100 - obj.sale) / 100
        #         self.cart.save()
        # for j in obj.users.all():
        #     print(j.id, self.cart.owner_id)
        #     if obj.code == request.POST['code'] and j.id != self.cart.owner_id:
        #         obj.users.add(self.cart.owner)
        #         self.cart.final_price = int(self.cart.final_price) * (100 - obj.sale) / 100
        #         self.cart.save()
        #         obj.save()
        #         return HttpResponseRedirect(reverse('basket'))


class order(CartMixin, generic.View):
    def get(self, request, *args, **kwargs):
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


class OrderAccept(CartMixin, generic.View):
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
            self.cart.owner.phone = req['tel']
            self.cart.owner.save()
        return HttpResponseRedirect(reverse('order'))

    def get(self, request, *args, **kwargs):
        # try:
        #     self.post(self, request, *args, **kwargs)
        # except AttributeError:
        return HttpResponseRedirect(reverse('index'))


class OrderPayment(CartMixin, generic.View):
    def post(self, request, *args, **kwargs):
        order = Order.objects.get(customer=self.cart.owner_id, cart=self.cart)
        order.status = 'in_progress'
        order.save()
        # for i in self.cart.products.all().filter(product__is_custom=True):
        #     i.product.delete()
        self.cart.in_order = True
        self.cart.save()
        return HttpResponseRedirect(reverse('index'))

    def get(self, request, *args, **kwargs):
        if not self.cart.products.all():
            return HttpResponseRedirect(reverse('index'))


class Custom(generic.TemplateView):
    template_name = 'custom.html'


def room(request):
    if request.user.is_superuser or request.user.is_staff:
        return render(request, 'staffOrder.html')
    else:
        return HttpResponseRedirect(reverse('index'))
