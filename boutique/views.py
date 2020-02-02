from django.shortcuts import render, get_object_or_404
from .models import Category, Item

# Create your views here.
def index(request):
    '''landing page'''
    categories = Category.objects.all()
    context = {'categories':categories}
    return render(request, 'boutique/index.html', context)