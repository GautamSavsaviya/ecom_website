from django.urls import path
from products.views import detail

app_name = "products"
urlpatterns = [
   path("<slug>/", detail, name="detail")
]