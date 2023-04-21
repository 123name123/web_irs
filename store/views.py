from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from .forms import RegisterForm, ProductSearchForm
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

from .product_db import DBProduct

from django.contrib.auth import authenticate, login, logout

# Create your views here.

db_use = DBProduct()


def register_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = RegisterForm()

    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + user)
            return redirect('login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("/")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="login.html", context={"form": form})


def logout_page(request):
    logout(request)
    return redirect("/")


def profile_page(request):
    return redirect("/")


def index(request):
    context = {'user': request.user, 'title': 'StoreName'}
    return render(request, 'base.html', context)


def product_catalog(request):
    form = ProductSearchForm(request.GET)

    page_number = int(request.GET.get('page', 1))
    products = list()
    name = ""
    product_per_page = 25
    next_page_number = 0
    if form.is_valid():
        name = form.cleaned_data['name']
        if name != "":
            products = db_use.get_products_by_name(name, page_number, product_per_page)
        if len(products) > 25:
            next_page_number = page_number + 1

    context = {'name': name,
               'products': products,
               'form': form,
               'page': page_number,
               'prev_page': page_number - 1,
               'next_page': next_page_number}
    return render(request=request, template_name="product_catalog.html", context=context)

    """print(request.POST)
    name = request.POST["product_name"]
    if request.method == "POST":
        products = []
        page = request.GET.get('page')
        print(page)
        if name != '':
            products = db_use.get_products_by_name(name, page)
        context = {'name': name, 'products': products}
        return render(request=request, template_name="product_catalog.html", context=context)

    context = {'name': ''}
    return render(request=request, template_name="product_catalog.html", context=context)"""


def product_profile(request, product_id):
    context = {'product_id': product_id}
    return render(request, template_name="product_profile.html", context=context)
