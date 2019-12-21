from django.urls import resolve


def main_menu_processor(request) -> dict:
    active_url = resolve(request.path).url_name

    menu_items = [
        {
            'name': 'Home',
            'url': 'info:home'
        },
        {
            'name': 'Features',
            'url': 'logout'
        },
        {
            'name': 'Reference',
            'url': 'logout'
        },
        {
            'name': 'Trade Hub',
            'url': 'logout'
        },
        {
            'name': 'Vote',
            'url': 'logout'
        },
        {
            'name': 'About',
            'url': 'logout'
        }
    ]

    for i, item in enumerate(menu_items):
        if item['url'] is active_url:
            menu_items[i]['is_active'] = True
        else:
            menu_items[i]['is_active'] = False

    return {'main_menu_items': menu_items}
