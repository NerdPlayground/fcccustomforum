from .models import Category
from django.contrib import admin

class CategoryAdmin(admin.ModelAdmin):
    fields=["title","description"]
    list_display=["title","pk","description","author"]

    def save_model(self,request,obj,form,change):
        obj.author=request.user
        super().save_model(request,obj,form,change)
    
    def has_change_permission(self,request,obj=None):
        if obj: return obj.author==request.user
        return True

    def has_delete_permission(self,request,obj=None):
        if obj: return obj.author==request.user
        return True

admin.site.register(Category,CategoryAdmin)