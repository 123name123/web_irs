from django.urls import path
from . import views
from django.conf.urls.static import static
from storeproject import settings

urlpatterns = [
    path('cart/', views.cart, name='cart')
]