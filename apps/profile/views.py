from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from main.libs.jsonapi import JsonAPI


@cache_page(60 * 1)
@vary_on_cookie
@login_required
def inventory(request):
    jsonapi = JsonAPI()
    inv = jsonapi.call('getPlayerInventory', [request.user.name])

    return render(request, 'profile/inventory.html', {'resp': inv})
