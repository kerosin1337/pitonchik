from django.views.generic import View

from .models import Cart, UserData


class CartMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = UserData.objects.filter(id=request.user.id).first()
            if not customer:
                customer = UserData.objects.create(id=request.user.id)
            cart = Cart.objects.filter(owner=customer, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer)
        else:
            if not request.session.session_key:
                request.session.save()
            customer = UserData.objects.filter(session=request.session.session_key).first()
            if not customer:
                customer = UserData.objects.create(session=request.session.session_key)
            cart = Cart.objects.filter(owner=customer, for_anonymous_user=True, in_order=False).first()
            if not cart:
                cart = Cart.objects.create(owner=customer, for_anonymous_user=True)
        self.cart = cart
        return super().dispatch(request, *args, **kwargs)
