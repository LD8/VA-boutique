from .models import Category
from django.template.context_processors import request


def category_context_processor(request):
    categories = Category.objects.get_categories_with_item().prefetch_related('subcategory_set')
    return {'categories': categories}
