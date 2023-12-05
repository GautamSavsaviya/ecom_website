from django.urls import path
from accounts.views import login_user, register_user, activate_account, logout_user, add_to_cart, cart, remove_cart_item, remove_coupon, payment_success

app_name = "accounts"
urlpatterns = [
    path("login/", login_user, name="login"),
    path("signup/", register_user, name="signup"),
    path("activate/<email_token>", activate_account, name="activate_account"),
    path("logout/", logout_user, name="logout"),
    path("add-cart/<uid>", add_to_cart, name="add_to_cart"),
    path("cart/", cart, name="cart"),
    path("remove-cart-item/<uid>", remove_cart_item, name="remove_cart_item"),
    path("remove-coupon/<uid>", remove_coupon, name="remove_coupon"),
    path("success/", payment_success, name="payment_success"),
]