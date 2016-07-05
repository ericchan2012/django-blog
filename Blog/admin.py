from django.contrib import admin

# Register your models here.

from .models import Article,Category,Tag,BlogComment

class ArticleAdmin(admin.ModelAdmin):
    fields = ['title', 'body','thumbnail','status','abstract','category','tags']

admin.site.register(Article,ArticleAdmin)

class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Category,CategoryAdmin)

class TagAdmin(admin.ModelAdmin):
    fields = ['name']

admin.site.register(Tag,TagAdmin)

class BlogCommentAdmin(admin.ModelAdmin):
    fields = ['user_name','user_email','body']

admin.site.register(BlogComment,BlogCommentAdmin)