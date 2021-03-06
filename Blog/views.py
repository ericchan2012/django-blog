# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from Blog.models import Article, Category, Tag, BlogComment
from Blog.forms import BlogCommentForm
from markdown import markdown
from django.views.generic.edit import FormView
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.db import connection


class IndexView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(status='p')
        for article in article_list:
            article.body = markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['navigation_list'] = Article.objects.all().order_by('name')
        kwargs['hotarticle_list'] = Article.objects.all().order_by('-views')[:8]
        kwargs['carouselarticle_list'] = Article.objects.all().order_by('-last_modified_time')[:3]
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['date_archive'] = Article.objects.archive()
        return super(IndexView, self).get_context_data(**kwargs)

class NavigationView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(navigation=self.kwargs['nav_id'], status='p')
        for article in article_list:
            article.body = markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['navigation_list'] = Article.objects.all().order_by('name')
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['hotarticle_list'] = Article.objects.all().order_by('-views')[:8]
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(NavigationView, self).get_context_data(**kwargs)

class CategoryView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        article_list = Article.objects.filter(category=self.kwargs['cate_id'], status='p')
        for article in article_list:
            article.body = markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['category_list'] = Category.objects.all().order_by('name')
        return super(CategoryView, self).get_context_data(**kwargs)


class TagView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        """
        根据指定的标签获取该标签下的全部文章
        """
        article_list = Article.objects.filter(tags=self.kwargs['tag_id'], status='p')
        for article in article_list:
            article.body = markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(TagView, self).get_context_data(**kwargs)


class ArticleDetailView(DetailView):
    model = Article
    template_name = "blog/detail.html"
    context_object_name = "article"
    pk_url_kwarg = 'article_id'

    def get_object(self):
        obj = super(ArticleDetailView, self).get_object()
        obj.body = markdown(obj.body, extras=['fenced-code-blocks'], )
        return obj
    #用来实现相关文章推荐
    def list_to_dic(self,resultlist):
        object_list = []
        for obj in resultlist:
            dic = {}
            dic['id'] = obj[0]
            dic['title'] = obj[1]
            object_list.append(dic)
        return object_list

    def relate_article(self,article_id, tags):
        in_where_str = "tag_id=" + str(tags[0])
        for i in range(1, len(tags)):
            in_where_str = in_where_str + " or tag_id=" + str(tags[i])
        out_where_str = "id!=" + str(article_id)
        sql = "select id,title from Blog_article as a,(select article_id,count(article_id) from Blog_article_tags where " + in_where_str + \
              " group by article_id order by count(article_id) desc limit 3) as tview where id=tview.article_id and " + out_where_str
        cursor = connection.cursor()
        cursor.execute(sql)
        resultlist = cursor.fetchall()
        return list_to_dic(resultlist)

    def get_context_data(self, **kwargs):
        kwargs['comment_list'] = self.object.blogcomment_set.all()
        kwargs['hotarticle_list'] = Article.objects.all().order_by('-views')[:8]
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        kwargs['category_list'] = Category.objects.all().order_by('name')
        kwargs['form'] = BlogCommentForm()
        # kwargs['relative_article_list'] = self.relate_article('article_id','tag_list')
        return super(ArticleDetailView, self).get_context_data(**kwargs)






class ArchiveView(ListView):
    template_name = "blog/index.html"
    context_object_name = "article_list"

    def get_queryset(self):
        # 接收从url传递的year和month参数，转为int类型
        year = int(self.kwargs['year'])
        month = int(self.kwargs['month'])
        # 按照year和month过滤文章
        article_list = Article.objects.filter(created_time__year=year, created_time__month=month)
        for article in article_list:
            article.body = markdown(article.body, extras=['fenced-code-blocks'], )
        return article_list

    def get_context_data(self, **kwargs):
        kwargs['tag_list'] = Tag.objects.all().order_by('name')
        return super(ArchiveView, self).get_context_data(**kwargs)


class CommentPostView(FormView):
    form_class = BlogCommentForm
    template_name = 'blog/detail.html'

    def form_valid(self, form):
        """提交的数据验证合法后的逻辑"""
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])

        comment = form.save(commit=False)

        comment.article = target_article
        comment.save()

        self.success_url = target_article.get_absolute_url()
        return HttpResponseRedirect(self.success_url)

    def form_invalid(self, form):
        """提交的数据验证不合法后的逻辑"""
        target_article = get_object_or_404(Article, pk=self.kwargs['article_id'])

        return render(self.request, 'blog/detail.html', {
            'form': form,
            'article': target_article,
            'comment_list': target_article.blogcomment_set.all(),
        })
