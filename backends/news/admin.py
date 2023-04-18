from django.contrib import admin

from .models import Category,News,NewsCharacters
class NewsAdmin(admin.ModelAdmin):
    list_display = ['title','create_time','category']
    search_fields = ['title']
    list_filter =  ['category']
    list_per_page = 20

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id','name']
    list_per_page = 20

class NewsCharactersAdmin(admin.ModelAdmin):
    list_display = ['news','keywords','visited']
    search_fields = ['keywords']
    list_per_page = 20

admin.site.register(News,NewsAdmin)
admin.site.register(Category,CategoryAdmin)
admin.site.register(NewsCharacters,NewsCharactersAdmin)