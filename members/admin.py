from .models import Member
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class MemberAdmin(UserAdmin):
    model=Member
    list_display=[
        "username","pk","first_name","last_name",
        "joined_in","email","is_staff","trust_level"
    ]
    fieldsets=[
        (None,{'fields':['username','password']}),
        ('Personal Info',{'fields':['first_name','last_name','email']}),
        ('Permissions',{'fields':['is_active','is_staff','is_superuser']}),
    ]
    
    def has_change_permission(self,request,obj=None):
        if obj: return obj==request.user
        return True

    def has_delete_permission(self,request,obj=None):
        if obj: return obj==request.user
        return True

admin.site.register(Member,MemberAdmin)