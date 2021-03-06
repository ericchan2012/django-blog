# -*- coding: UTF-8 -*-
from __future__ import unicode_literals

from django.db import models
from collections import defaultdict
from django.core.urlresolvers import reverse


UPLOAD_ROOT = 'upload'

class ArticleManage(models.Manager):
    """
    继承自默认的 Manager ，为其添加一个自定义的 archive 方法
    """

    def archive(self):
        date_list = Article.objects.datetimes('created_time', 'month', order='DESC')
        date_dict = defaultdict(list)
        for d in date_list:
            date_dict[d.year].append(d.month)
        return sorted(date_dict.items(), reverse=True)


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', u'草稿'),
        ('p', u'发布'),
    )

    NAVIGATION_CHOICES = (
        ('0', u'新闻'),
        ('1', u'教程'),
        ('2', u'资源'),
    )
    title = models.CharField('标题', max_length=70)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES,default=STATUS_CHOICES[1][0])
    navigation = models.CharField('导航名字', max_length=1, choices=NAVIGATION_CHOICES, default=NAVIGATION_CHOICES[0][0])
    abstract = models.CharField('摘要', max_length=150, blank=True, null=True,
                                help_text="可选，如若为空将摘取正文的前150个字符")
    views = models.PositiveIntegerField('浏览量', default=0)
    likes = models.PositiveIntegerField('点赞数', default=0)
    topped = models.BooleanField('置顶', default=False)
    thumbnail = models.ImageField('封面',upload_to='upload/thumbnail')

    category = models.ForeignKey('Category', verbose_name='经典教程类别',
                                 null=True,
                                 on_delete=models.SET_NULL)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    objects = ArticleManage()

    def __unicode__(self):
        return u'%s' % self.title

    class Meta:
        ordering = ['-last_modified_time']

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.pk})
#for 经典教程
class Category(models.Model):
    name = models.CharField('经典教程类名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return u'%s' % self.name


class Tag(models.Model):
    """
    tag(标签)对应的数据库model
    """
    name = models.CharField('标签名', max_length=20)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_modified_time = models.DateTimeField('修改时间', auto_now=True)

    def __unicode__(self):
        return u'%s' % self.name


class BlogComment(models.Model):
    user_name = models.CharField('评论者名字', max_length=100)
    user_email = models.EmailField('评论者邮箱', max_length=255)
    body = models.TextField('评论内容')
    created_time = models.DateTimeField('评论发表时间', auto_now_add=True)
    article = models.ForeignKey('Article', verbose_name='评论所属文章', on_delete=models.CASCADE)

    def __unicode__(self):
        return u'%s' % self.body[:20]
