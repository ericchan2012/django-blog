# -*- coding: UTF-8 -*-
from django.contrib import admin

from .models import Article, Category, Tag, BlogComment
from pagedown.widgets import AdminPagedownWidget
from django import forms
# from  DjangoUeditor.forms import UEditorField

class ArticleForm(forms.ModelForm):
    body = forms.CharField(widget=AdminPagedownWidget())
    # body = UEditorField('content',height=100,width=500,imagePath="upload/thumbnail/",toolbars='mini',filePath='upload')

    class Meta:
        model = Article
        fields = '__all__'

class ArticleAdmin(admin.ModelAdmin):
    form = ArticleForm

# class ArticleAdmin(admin.ModelAdmin):
#     # fields = ['title', 'body', 'thumbnail', 'status', 'abstract', 'navigation', 'category', 'tags']
#     fields = '__all__'

admin.site.register(Article, ArticleAdmin)


class CategoryAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(Category, CategoryAdmin)


class TagAdmin(admin.ModelAdmin):
    fields = ['name']


admin.site.register(Tag, TagAdmin)


class BlogCommentAdmin(admin.ModelAdmin):
    fields = ['user_name', 'user_email', 'body']


admin.site.register(BlogComment, BlogCommentAdmin)
