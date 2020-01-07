from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from main.libs.jsonapi.core import JsonAPI
from main.libs.jsonapi.inventory import add_data_to_items, change_inv_format


@cache_page(60 * 1)
@vary_on_cookie
@login_required
def inventory(request):
    skin_url = f"https://visage.surgeplay.com/full/344/{request.user.uuid.hex}.png"

    jsonapi = JsonAPI()
    jsonapi.add_url('getPlayerInventory', [request.user.name])\
           .add_url('getPlayerEnderchest', [request.user.name])\
           .add_url('econ.getBalance', [request.user.name])

    results = jsonapi.call()
    inv, ender, balance = results[0], results[1], results[2]

    # Inventory
    add_data_to_items(inv['inventory'])
    change_inv_format(inv)

    # Enderchest
    add_data_to_items(ender)

    return render(request, 'profile/inventory.html', {
        'inv': inv,
        'ender': ender,
        'balance': balance,
        'skin_url': skin_url
    })
