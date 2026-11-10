from django.contrib import admin
from .models import Category, Listing, Application, Review

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(Application)
admin.site.register(Review)