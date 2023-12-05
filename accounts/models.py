from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_activation_mail
from products.models import Product, ColorVariant, SizeVariant, Coupon
from django.contrib import messages


# Create your models here.


class Profile(BaseModel):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(upload_to="profile")
    email_token = models.CharField(max_length=100, null=True, blank=True)
    is_email_verified = models.BooleanField(default=False)


    def get_cart_count(self):
        return CartItem.objects.filter(cart__is_paid = False, cart__user=self.user).count()


class Cart(BaseModel):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="cart")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    is_paid = models.BooleanField(default=False)
    razor_pay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razor_pay_payment_signature = models.CharField(max_length=100, null=True, blank=True)



    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'
    

    def get_total_price(self):
        price = []

        for item in self.cart_items.all():
            price.append(item.product.price)

            if item.color_variant:
                price.append(item.color_variant.price)
            if item.size_variant:
                price.append(item.size_variant.price)  

        if self.coupon:
            if sum(price) > self.coupon.minimum_amount:
                return sum(price) - self.coupon.discount_price
            else:
                self.coupon = None
                self.save()
        return sum(price)



class CartItem(BaseModel):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL, null=True, blank=True)
    color_variant = models.ForeignKey(
        ColorVariant, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(
        SizeVariant, on_delete=models.SET_NULL, null=True, blank=True)
    
    def get_product_price(self):
        price = [self.product.price]

        if self.color_variant:
            price.append(self.color_variant.price)
        if self.size_variant:
            price.append(self.size_variant.price)
        
        return sum(price)


@receiver(post_save, sender=User)
def send_email_token(sender, instance, created, **kwargs):
    try:
        if created:
            email = instance.email
            email_token = str(uuid.uuid4())
            Profile.objects.create(user=instance, email_token=email_token)
            send_account_activation_mail(email, email_token)

    except Exception as e:
        print(e)
