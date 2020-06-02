from django.contrib import admin
from django.urls import path, include
from . import settings
from django.contrib.staticfiles.urls import static, staticfiles_urlpatterns
import os
from boutique import sitemaps
from django.contrib.sitemaps.views import sitemap

sitemaps = {
    'static': sitemaps.StaticViewSitemap,
    'category': sitemaps.CategoryViewSitemap,
    'subcategory': sitemaps.SubCategoryViewSitemap,
    'item': sitemaps.ItemViewSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    # SEO
    path('robots.txt', include('robots.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps},
         name='django.contrib.sitemaps.views.sitemap'),

    path('', include('boutique.urls')),
    path('users/', include('users.urls')),
    path('shopping/', include('shopping.urls')),
    path('wishlist/', include('wishlist.urls')),
    path('vip/', include('vip.urls')),
]

# make sure static files can be loaded locally
if not os.environ.get('USE_PROD_DB', None):
    urlpatterns += staticfiles_urlpatterns()
    # this basically tells 'urlpatterns' what media url to add and where media files are
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)

    import debug_toolbar
    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)), ] + urlpatterns
