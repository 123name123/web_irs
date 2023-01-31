from django.urls import path, include
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_page, name='register'),
    path('catalog/', views.product_catalog, name='catalog'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('product/<int:product_id>/', views.product_profile, name='product'),
]
