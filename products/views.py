from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views.generic import ListView

from products.models import Product

class ProductList(LoginRequiredMixin, ListView):
    template_name = "products/list.html"
    model = Product
    queryset = Product.objects.all()