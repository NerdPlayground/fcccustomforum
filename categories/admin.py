from .models import Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    fields=["title","description"]
    list_display=["title","pk","description","author"]

    def save_model(self,request,obj,form,change):
        obj.author=request.user
        super().save_model(request,obj,form,change)

admin.site.register(Category,CategoryAdmin)