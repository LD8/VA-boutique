from django import template

# To be a valid tag library, the module must contain a module-level variable named register that is a template.Library instance, 
# in which all the tags and filters are registered.
register = template.Library()

@register.simple_tag(takes_context=True)
def item_is_valid(context, item):
    brand_selected = context['filter_context'].get('brand_selected')
    min_price = context['filter_context'].get('min_price')
    if min_price == '' or min_price is None:
        min_price = 0
    max_price = context['filter_context'].get('max_price')
    if max_price == '' or max_price is None:
        max_price = 999999

    if int(min_price) <= item.final_price < int(max_price):
        # if the min/max is None or item's price is in range
        if brand_selected is None or brand_selected=='бренд' or item.brand.name == brand_selected:
            # if no brand is selected or ...
            return True
        else:
            return False
        