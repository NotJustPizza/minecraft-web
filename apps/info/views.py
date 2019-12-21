from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page


@cache_page(60 * 15)
def home(request):
    return render(request, 'info/home.html')
