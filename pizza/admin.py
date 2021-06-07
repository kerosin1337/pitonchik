from django.contrib import admin

from . import models

admin.site.site_header = 'У Альбертовича'
admin.site.register(models.UserData)
admin.site.register(models.Category)
admin.site.register(models.Products)
admin.site.register(models.Promotions)
admin.site.register(models.CartProduct)
admin.site.register(models.Cart)
admin.site.register(models.Order)
admin.site.register(models.Coupon)
