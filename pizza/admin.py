from django.contrib import admin

from .models import *

admin.site.site_header = 'У Альбертовича'
admin.site.register(UserData)
admin.site.register(Category)
admin.site.register(Products)
admin.site.register(CartProduct)
admin.site.register(Cart)
admin.site.register(Order)
admin.site.register(Coupon)
