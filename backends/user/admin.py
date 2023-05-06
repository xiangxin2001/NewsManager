from django.contrib import admin
 # 1. 导入默认UserAdmin 作为Base Class
from .models import User,UserCharacters

class UserAdminPage(admin.ModelAdmin):
    list_display = ['uid','username','mobile','email','is_superuser']
    search_fields = ['username']
    list_filter =  ['is_superuser']
    list_per_page = 20
class UserCharactersAdminPage(admin.ModelAdmin):
    list_display = ['news_keyword','news_history','news_categroy_Poi','similar_users','user']
    search_fields = ['news_keyword']
    list_per_page = 20

admin.site.register(User,UserAdminPage)
admin.site.register(UserCharacters,UserCharactersAdminPage)