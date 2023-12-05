from django.contrib import admin
from products.models import Category, Product, ProductImage, ColorVariant, SizeVariant, Coupon

# Register your models here.
admin.site.register(Category)


class ProductImageAdmin(admin.StackedInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["product_name", "price"]
    inlines = [ProductImageAdmin]


@admin.register(ColorVariant)
class ColorVarinatAdmin(admin.ModelAdmin):
    model = ColorVariant
    list_display = ["color_name", "price"]


@admin.register(SizeVariant)
class ColorVarinatAdmin(admin.ModelAdmin):
    model = SizeVariant
    list_display = ["size_name", "price"]



@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ["coupon_code", "discount_price"]
admin.site.register(ProductImage)
# admin.site.register(Coupon)
