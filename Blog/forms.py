# -*- coding: UTF-8 -*-
from django import forms
from .models import Article, BlogComment

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment

        fields = ['user_name', 'user_email', 'body']

        widgets = {

            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入昵称必须填",
                'aria-describedby': "sizing-addon1",
            }),
            'user_email': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "请输入邮箱必须填",
                'aria-describedby': "sizing-addon1",
            }),
            'body': forms.Textarea(attrs={'placeholder': '我来评两句必须填'}),
        }