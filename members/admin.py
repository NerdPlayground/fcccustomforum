from .models import Member
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

class MemberAdmin(UserAdmin):
    model=Member
    list_display=["username","joined_in","email","is_staff","trust_level"]
    add_fieldsets=UserAdmin.add_fieldsets+((None,{'fields':('email',)}),)

admin.site.register(Member,MemberAdmin)