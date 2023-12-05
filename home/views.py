from django.shortcuts import render
from products.models import Product
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required(login_url="accounts:login")
def index(request):
    products = Product.objects.all()
    context = {
        'products': products
    }
    return render(request, "home/index.html", context)
