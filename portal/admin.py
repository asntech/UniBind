## Author: Aziz Khan
## License: GPL v3
## Copyright 2017 Aziz Khan <azez.khan__AT__gmail.com>

from django.contrib import admin

from .models import Factor, FactorData, Post


class FactorAdmin(admin.ModelAdmin):
	list_display = ('tf_name', 'cell_line','folder','data_source')
	search_fields = ['tf_name', 'cell_line', 'id','biological_condition','folder','data_source']
	list_filter = ('tf_name', 'data_source',)

admin.site.register(Factor, FactorAdmin)


class NewsAndUpdateAdmin(admin.ModelAdmin):
	list_display = ('title', 'author','category','date')
	search_fields = ['title', 'author','category']
	list_filter = ('category','author',)

admin.site.register(Post, NewsAndUpdateAdmin)