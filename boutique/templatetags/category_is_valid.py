from django import template
from boutique.models import Item

register = template.Library()

@register.simple_tag(takes_context=True)
def category_is_valid(context, category):

    categories_validated = context['filter_context'].get('categories_validated')
    subcategories_validated = context['filter_context'].get('subcategories_validated')

    if category.name in categories_validated or category.name in subcategories_validated:
        return True
    else:
        return False