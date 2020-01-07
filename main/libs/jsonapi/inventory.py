from django.templatetags.static import static


# Adds important data to items from API response
def add_data_to_items(items: list) -> None:
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
            # If there is no item then placeholder and set it's image to air
            items[i] = {}
            items[i]['image_url'] = static('img/depixel/item_or_block/air.png')


def change_inv_format(inv: dict):
    # Adjust order of slots
    armor_slots = inv['inventory'][36:40][::-1]
    shield_slot = inv['inventory'][40]
    hotbar_slots = inv['inventory'][:9]
    storage_slots = inv['inventory'][9:36]

    inv['inventory'] = storage_slots + hotbar_slots
    # Override armor data from API
    inv['armor'] = armor_slots + [shield_slot]
