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

admin.site.register(Topic,TopicAdmin)