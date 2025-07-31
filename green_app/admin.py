from django.contrib import admin
from .models import Category, GreenIdea, Newsletter

admin.site.register(Category)
admin.site.register(GreenIdea)
admin.site.register(Newsletter)