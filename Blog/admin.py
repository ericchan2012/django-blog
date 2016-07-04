from django.contrib import admin

# Register your models here.

from .models import Article,Category

class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'body','status','abstract','category']

admin.site.register(Article,ArticleAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Category,CategoryAdmin)