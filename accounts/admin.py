from django.contrib import admin
from accounts.models import Profile, Cart, CartItem

# Register your models here.
admin.site.register(Profile)

admin.site.register(Cart)

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ["cart", "product", "size_variant", "color_variant"]
