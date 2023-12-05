from django.shortcuts import render
from django.http import HttpResponseRedirect
from products.models import Product, SizeVariant, ColorVariant
from accounts.models import Cart, CartItem
from django.contrib.auth.decorators import login_required


# Create your views here.
@login_required(login_url="accounts:login")
def detail(request, slug):
    try:
        product = Product.objects.get(slug=slug)
        context = {
            'product': product
        }

        if request.method == "GET":
            size = request.GET.get("size", "")
            color = request.GET.get("color", "")
            price = product.get_product_price_by_variant(size, color)
            context['updated_price'] = price
            context['selected_size'] = size
            context['selected_color'] = color

    except Exception as e:
        print(e)
    return render(request, "products/detail.html", context)
