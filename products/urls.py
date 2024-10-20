from django.urls import path

from .views import *

urlpatterns = [
    path("product/list/", ProductList.as_view()),
]