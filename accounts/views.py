from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from accounts.models import Profile, Cart, CartItem
from products.models import Coupon, Product, ColorVariant, SizeVariant
import razorpay
from django.conf import settings
from django.contrib.auth.decorators import login_required
from base.helpers import save_invoice_pdf

# Create your views here.


def register_user(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        user_obj = User.objects.filter(username=email)

        if user_obj.exists():
            messages.error(request, "User already exist.")
            return HttpResponseRedirect(request.path)

        if password2 != password1:
            messages.error(request, "Both password must be same.")
            return HttpResponseRedirect(request.path)

        user_obj = User.objects.create(
            username=email, email=email, first_name=first_name, last_name=last_name)
        user_obj.set_password(password1)
        user_obj.save()
        messages.success(
            request, "An email has been sent on your mail to varify your email.")
        return HttpResponseRedirect(request.path)

    return render(request, "accounts/register.html")


def login_user(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_obj = User.objects.filter(username=email)

        if not user_obj.exists():
            messages.error(request, "User does not exist.")
            return HttpResponseRedirect(request.path)

        if not user_obj[0].profile.is_email_verified:
            messages.error(
                request, "User is not verified, First you need to verify by clicking the link sent to your mail.")
            return HttpResponseRedirect(request.path)

        user_obj = authenticate(username=email, password=password)

        if user_obj:
            login(request, user_obj)
            return redirect("/")
        else:
            messages.error(request, "Invalid username or password.")
            return HttpResponseRedirect(request.path)

    return render(request, "accounts/login.html")


def activate_account(request, email_token):
    try:
        user_obj = Profile.objects.get(email_token=email_token)
        user_obj.is_email_verified = True
        user_obj.save()
        return redirect("accounts:login")
    except Exception as e:
        print(e)
        return HttpResponse("<h1>Invalid token link try letter...!</h1>")


# @login_required(login_url="accounts:login")
def logout_user(request):
    try:
        logout(request)
        return redirect('home:index')
    except Exception as e:
        print(e)
        return HttpResponse("There is some error, please try leter...!")


@login_required(login_url="accounts:login")
def add_to_cart(request, uid):
    user = request.user
    product = Product.objects.get(uid=uid)
    size = request.GET.get("size")
    color = request.GET.get("color")
    cart, _ = Cart.objects.get_or_create(user=user, is_paid=False)

    cart_item = CartItem.objects.create(cart=cart, product=product)

    if size:
        size_variant = SizeVariant.objects.get(size_name=size)
        cart_item.size_variant = size_variant
        cart_item.save()
    if color:
        color_variant = ColorVariant.objects.get(color_name=color)
        cart_item.color_variant = color_variant
        cart_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@login_required(login_url="accounts:login")
def cart(request):
    cart_obj = None
    try:
        cart_obj = Cart.objects.get(is_paid=False, user=request.user)
    except Exception as e:
        print(e)

    if request.method == "POST":
        coupon = request.POST.get("coupon")

        coupon_obj = Coupon.objects.filter(coupon_code=coupon)

        if not coupon_obj.exists():
            messages.error(request, "Invalid coupon code.")
            return redirect("accounts:cart")

        if cart_obj.coupon:
            messages.warning(request, "Coupon alredy applied.")
            return redirect("accounts:cart")

        if cart_obj.get_total_price() < coupon_obj[0].minimum_amount:
            messages.warning(
                request, f"Minimum amount to apply this coupon is {coupon_obj[0].minimum_amount}")
            return redirect("accounts:cart")

        if coupon_obj[0].is_expired:
            messages.warning(request, "Coupon has been expired.")
            return redirect("accounts:cart")

        cart_obj.coupon = coupon_obj[0]
        cart_obj.save()
        messages.success(request, "Coupon applied.")
        return redirect("accounts:cart")

    if cart_obj is not None:
        client = razorpay.Client(auth=(settings.KEY_ID, settings.KEY_SECRET))
        payment = client.order.create(
            {'amount': cart_obj.get_total_price()*100, 'currency': 'INR', 'payment_capture': 1})

        cart_obj.razor_pay_order_id = payment['id']
        cart_obj.save()

        context = {
            'cart': cart_obj,
            'payment': payment,
        }
    else:
        context = {
            'cart': cart_obj,
        }

    return render(request, 'accounts/cart.html', context)


@login_required(login_url="accounts:login")
def remove_cart_item(request, uid):
    try:
        cart_item = CartItem.objects.get(uid=uid)
        cart_item.delete()
    except Exception as e:
        print(e)
    return redirect("accounts:cart")


@login_required(login_url="accounts:login")
def remove_coupon(request, uid):
    cart_obj = Cart.objects.get(uid=uid)
    cart_obj.coupon = None
    cart_obj.save()

    messages.success(request, "Coupon removed.")
    return redirect("accounts:cart")


@login_required(login_url="accounts:login")
def payment_success(request):
    order_id = request.GET.get("order_id")
    payment_id = request.GET.get("payment_id")
    payment_signature = request.GET.get("payment_signature")

    cart_obj = Cart.objects.get(razor_pay_order_id=order_id)

    cart_obj.razor_pay_payment_id = payment_id
    cart_obj.razor_pay_payment_signature = payment_signature
    cart_obj.is_paid = True
    cart_obj.save()

    context = {
        'user': cart_obj.user,
        'cart':cart_obj
    }

    save_invoice_pdf(context)

    return redirect("accounts:cart")
