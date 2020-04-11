"""jbt_blog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, reverse_lazy
from apps.blog import views
from apps.comment import views as comment_view
from django.conf.urls import include
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.contrib.auth import views as contrib_auth_views
from werobot.contrib.django import make_view
from apps.blog.robot import robot

urlpatterns = [
    path(r'admin/', admin.site.urls),
    path(r'', views.home, name='home'),
    path(r'home/', views.home, name='home'),
    path(r'articles/', views.articles, name='articles'),
    path(r'accounts/login/', contrib_auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path(r'accounts/logout/', contrib_auth_views.LogoutView.as_view(next_page=reverse_lazy('login')),
        name='logout'),
    path(r'articles/<int:id>/', views.detail, name='detail'),
    path(r'category/<int:id>/', views.search_category, name='category_menu'),
    path(r'tag/<str:tag>/', views.search_tag, name='search_tag'),
    path(r'archives/<str:year>/<str:month>', views.archives, name='archives'),
    path(r'summernote/', include('django_summernote.urls')),
    path(r'jet/', include('jet.urls', 'jet')),  # Django JET URLS
    path(r'jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')),  # Django JET dashboard URLS
    path(r'image/upload', views.uploadImg, name='uploadImg'),
    path(r'image/show', views.showImg, name='showImg'),
    path(r'post-comment/<int:id>/', comment_view.post_comment, name='post_comment'),
    path(r'robot/',make_view(robot)),
    path(r'mdeditor/', include('mdeditor.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
else:
    urlpatterns += [
        url(r'^static/(?P<path>.*)$', serve,
            {'document_root': settings.STATIC_ROOT, 'show_indexes': settings.DEBUG})
    ]