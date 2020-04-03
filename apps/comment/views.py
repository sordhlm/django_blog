import base64
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, QueryDict
from apps.blog.models import Article
from apps.comment.forms import CommentForm
# Create your views here.
def post_comment(request, id):
    article = get_object_or_404(Article, id=id)

    # 处理 POST 请求
    if request.method == 'POST':
        ip = base64.b64encode(request.META['REMOTE_ADDR'].encode())
        data = QueryDict(mutable=True)
        data.update(request.POST)
        data.update({'user': 'Guest'+'_'+ip.decode()})
        print(data)
        comment_form = CommentForm(data)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.article = article
            new_comment.save()
            return redirect(article)
        else:
            #print(comment_form.clean_data)
            print(comment_form.errors.as_data())
            return HttpResponse("表单内容有误，请重新填写。")
    # 处理错误请求
    else:
        return HttpResponse("发表评论仅接受POST请求。")