from .models import Reply
from django.contrib import admin

class ReplyAdmin(admin.ModelAdmin):
    fields=["topic","content"]
    list_display_links=["content"]
    list_display=["member","pk","topic","content","created_at","updated_at"]

    def save_model(self,request,obj,form,change):
        obj.member=request.user
        super().save_model(request,obj,form,change)
    
    def has_change_permission(self,request,obj=None):
        if obj: return obj.member==request.user
        return True

    def has_delete_permission(self,request,obj=None):
        if obj: return obj.member==request.user
        return True

admin.site.register(Reply,ReplyAdmin)