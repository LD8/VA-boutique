from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Category, SubCategory


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['index', 'sales', 'new', 'women', 'men']

    def location(self, item):
        return reverse(item)


class CategoryViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'monthly'

    def items(self):
        return Category.objects.all()


class SubCategoryViewSitemap(Sitemap):
    priority = 0.8
    changefreq = 'weekly'

    def items(self):
        return SubCategory.objects.all()


class ItemViewSitemap(Sitemap):
    priority = 0.7
    changefreq = 'daily'

    def items(self):
        return Item.objects.all()
