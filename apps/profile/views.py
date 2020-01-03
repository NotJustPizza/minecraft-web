from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.contrib.auth.decorators import login_required
from django.templatetags.static import static
from main.libs.jsonapi import JsonAPI


@cache_page(60 * 1)
@vary_on_cookie
@login_required
def inventory(request):
    def update_items(items: list):
        for i, item in enumerate(items):
            if item:
                # Give every item its static link
                items[i]['image_url'] = static(f"img/depixel/item_or_block/{item['type'].lower()}.png")
                # Give every item its slot_id
                items[i]['slot_id'] = i
                # Calculate durability percentage
                if item['durability'] > 0:
                    durability_max = 300  # To be added to API
                    durability_percent = round((durability_max - item['durability']) / durability_max * 100)
                    items[i]['durability_percent'] = durability_percent
                    if durability_percent < 30:
                        items[i]['durability_class'] = 'bg-danger'
                    elif durability_percent < 60:
                        items[i]['durability_class'] = 'bg-warning'
                    else:
                        items[i]['durability_class'] = 'bg-success'
            else:
                items[i] = {}
                items[i]['image_url'] = static('img/depixel/item_or_block/air.png')

    jsonapi = JsonAPI()

    # Inventory
    inv = jsonapi.call('getPlayerInventory', [request.user.name])
    update_items(inv['inventory'])

    # Adjust order of slots
    armor_slots = inv['inventory'][36:40][::-1]
    shield_slot = inv['inventory'][40]
    hotbar_slots = inv['inventory'][:9]
    storage_slots = inv['inventory'][9:36]

    inv['inventory'] = storage_slots + hotbar_slots
    # Override armor from API
    inv['armor'] = armor_slots + [shield_slot]

    # Enderchest
    ender = jsonapi.call('getPlayerEnderchest', [request.user.name])
    update_items(ender)

    # Skin API
    skin_url = f"https://crafatar.com/renders/body/{request.user.uuid}?scale=8"

    return render(request, 'profile/inventory.html', {'inv': inv, 'ender': ender, 'skin_url': skin_url})
