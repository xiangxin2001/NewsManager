from django.contrib import admin
 # 1. 导入默认UserAdmin 作为Base Class
from .models import User

class UserAdminPage(admin.ModelAdmin):
    list_display = ['uid','username','mobile','email','is_superuser']
    search_fields = ['username']
    list_filter =  ['is_superuser']
    list_per_page = 20


admin.site.register(User,UserAdminPage)