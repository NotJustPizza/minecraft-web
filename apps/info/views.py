from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from ipware import get_client_ip


#@cache_page(60 * 15)
def home(request):
    client_ip, _ = get_client_ip(request)

    return render(request, 'info/home.html', {'ip': client_ip})
