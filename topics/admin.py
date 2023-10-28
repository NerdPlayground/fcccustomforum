from .models import Topic
from django.contrib import admin

class TopicAdmin(admin.ModelAdmin):
    fields=["category","title","content"]
    list_display=[
        "title","pk","category","author",
        "created_at","updated_at","content","solved"
    ]

    def save_model(self,request,obj,form,change):
        obj.author=request.user
        super().save_model(request,obj,form,change)
    
    def has_change_permission(self,request,obj=None):
        if obj: return obj.author==request.user
        return True

    def has_delete_permission(self,request,obj=None):
        if obj: return obj.author==request.user
        return True

admin.site.register(Topic,TopicAdmin)