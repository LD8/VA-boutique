from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse
from .models import Category, SubCategory, Item


class StaticViewSitemap(Sitemap):
    priority = 0.9
    changefreq = 'monthly'

    def items(self):
        return ['boutique:index', 'boutique:sales', 'boutique:new']

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
