from typing import Iterable, Optional
from django.db import models
from django.db.models import CharField

from base.models import BaseModel
from django.utils.text import slugify


# Create your models here.


class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, blank=True, null=True)
    category_image = models.ImageField(upload_to="category")

    def save(self, *args, **kwagrs):
        self.slug = str(slugify(self.category_name))
        return super(Category, self).save(*args, **kwagrs)

    def __str__(self) -> str:
        return self.category_name


class ColorVariant(BaseModel):
    color_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.color_name


class SizeVariant(BaseModel):
    size_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.size_name


class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="product")
    slug = models.SlugField(unique=True, blank=True, null=True)
    product_description = models.TextField()
    price = models.IntegerField()
    color_variant = models.ManyToManyField(ColorVariant, blank=True)
    size_variant = models.ManyToManyField(SizeVariant, blank=True)

    def save(self, *args, **kwargs):
        self.slug = str(slugify(self.product_name))
        return super(Product, self).save(*args, **kwargs)

    def __str__(self) -> CharField:
        return self.product_name

    def get_product_price_by_variant(self, size, color):
        size_price = 0
        color_price = 0
        if SizeVariant.objects.filter(size_name=size):
            size_price = SizeVariant.objects.filter(size_name=size)[0].price
        if ColorVariant.objects.filter(color_name=color):
            color_price = ColorVariant.objects.filter(color_name=color)[0].price

        return self.price + size_price + color_price


class ProductImage(BaseModel):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_images")
    image = models.ImageField(upload_to="product")


class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=15)
    is_expired = models.BooleanField(default=False)
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

    def __str__(self) -> str:
        return self.coupon_code