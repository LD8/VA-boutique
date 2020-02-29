from django.shortcuts import reverse
from django.test import TestCase
from django.urls import get_resolver


class WebPagesTests(TestCase):

    def test_static_pages(self):
        urls = get_resolver(None).reverse_dict.keys()
        #urls = ['get_started', 'website_about', 'website_hiring',
        #            'terms_of_service', 'privacy_policy']
        for url in urls:
            url = reverse(url)
            resp = self.client.get(url)
            self.assertEqual(resp.status_code, 200)