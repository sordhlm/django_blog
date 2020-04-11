import re
import markdown
from django.shortcuts import render
from apps.blog.models import Article, Category, Tag, Image
from apps.comment.models import Comment
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings
from django.contrib import auth
from django.template import RequestContext
from django.contrib.auth.decorators import login_required


categories = Category.objects.all()  # 获取全部的分类对象
tags = Tag.objects.all()  # 获取全部的标签对象
months = Article.objects.datetimes('pub_time', 'month', order='DESC')


# Create your views here.
def home(request):  # 主页
    return render(request, 'front.html')

def articles(request):  # 主页
    posts = Article.objects.filter(status='p', pub_time__isnull=False)  # 获取全部(状态为已发布，发布时间不为空)Article对象
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'home.html', {'post_list': post_list, 'category_list': categories, 'months': months})



def detail(request, id):
    try:
        post = Article.objects.get(id=str(id))
        post.viewed()  # 更新浏览次数
        comments = Comment.objects.filter(article=str(id))
        tags = post.tags.all()
        next_post = post.next_article()  # 上一篇文章对象
        prev_post = post.prev_article()  # 下一篇文章对象
        post.content = markdown.markdown(post.content,
                                  extensions=[
                                     'markdown.extensions.extra',
                                     'markdown.extensions.codehilite',
                                     'markdown.extensions.toc',
                                  ])
    except Article.DoesNotExist:
        raise Http404
    return render(
        request, 'post.html',
        {
            'post': post,
            'tags': tags,
            'comments': comments,
            'category_list': categories,
            'next_post': next_post,
            'prev_post': prev_post,
            'months': months
        }
    )


def search_category(request, id):
    posts = Article.objects.filter(category_id=str(id))
    category = categories.get(id=str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html',
                  {'post_list': post_list,
                   'category_list': categories,
                   'category': category,
                   'months': months
                  }
    )


def search_tag(request, tag):
    posts = Article.objects.filter(tags__name__contains=tag)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tag.html', {
        'post_list': post_list,
        'category_list': categories,
        'tag': tag,
        'months': months
        }
    )


def archives(request, year, month):
    posts = Article.objects.filter(pub_time__year=year, pub_time__month=month).order_by('-pub_time')
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量
    try:
        page = request.GET.get('page')  # 获取URL中page参数的值
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'archive.html', {
        'post_list': post_list,
        'category_list': categories,
        'months': months,
        'year_month': year+'年'+month+'月'
        }
    )

def uploadImg(request):
    if request.method == 'POST':
        new_img = Image(
            img = request.FILES.get('img'),
            name = re.sub('\.\w+', '', request.FILES.get('img').name),
            description = request.POST.get('descript')
        )
        new_img.save()
    imgs = Image.objects.all()
    content = {
        'imgs':imgs,
    }
    return render(request, 'showimg.html', content)

def showImg(request):
    content = {}
    imgs = Image.objects.all()
    content = {
        'imgs':imgs,
    }
    return render(request, 'showimg.html', content)
