from django.contrib import sitemaps
from django.urls import reverse

class StaticViewSitemap(sitemaps.Sitemap):
    priority = 0.5
    changefreq = 'weekly'

    def items(self):
        return ['index', 'about', 'faq', 'search', 'documentation', 'contact_us','download_data', 'api_documentation']

    def location(self, item):
        return reverse(item)