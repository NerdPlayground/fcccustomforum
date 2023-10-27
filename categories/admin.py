from .models import Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    list_display=["title","pk","description","author"]

admin.site.register(Category,CategoryAdmin)