from django.contrib import admin
from .models import Article, Category, Tag, Image
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.

admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(Image)

class PostAdmin(SummernoteModelAdmin):
    summernote_fields = ('content',)  # 给content字段添加富文本


admin.site.register(Article, PostAdmin)