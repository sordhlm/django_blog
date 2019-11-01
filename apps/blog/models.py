from django.db import models
from django.utils.timezone import now


# Create your models here.
class User(models.Model):
    id = models.AutoField(db_column='uid', primary_key=True)
    source = models.CharField(verbose_name='source id', max_length=256)
    name = models.CharField(verbose_name='source id', max_length=256, default="")
    description = models.TextField(blank=True)
    mode = models.IntegerField(db_column='mode', default=0)#0: default; 1: chat; 2: poem_type; 3: poem_init; 4: poem_create
    thrd = models.IntegerField(db_column='threshold', default=12)
    ptype = models.CharField(max_length=16, default='5jue')
    pinit = models.CharField(max_length=256, default="")
    # 使对象在后台显示更友好
    def __str__(self):
        return self.source

    class Meta:
        unique_together = ('source', 'name')
        verbose_name_plural = 'source id'  # 指定后台显示模型复数名称

    @classmethod
    def room_choose(cls, user, mode=1):
        user.mode = mode
        user.save()
        return r"请从选择你要进入的木屋哪个房间:\n 0)草庐弄诗；\n 1）茶室外话"

    @classmethod
    def enter_chat(cls, user, mode=2, out='leave'):
        user.mode = mode
        user.save()
        ret = r"欢迎进入茶室，你可以和Vena英语对话啦，请输入'%s'离开房间"%out
        return ret

    @classmethod
    def enter_poem(cls, user, mode=3, out='leave'):
        user.mode = mode
        user.save()
        ret = r"欢迎进入草庐，你可以作诗啦， 请输入'%s'离开房间"%out
        ret += r"请从选择诗的类型:\n 0）五绝\n 1）七绝\n2）直接开始"
        return ret

    @classmethod
    def cfg_poem_type(cls, user, ptype, mode=4):
        user.mode = mode
        user.ptype = ptype
        user.save()
        ret = r"poem type is 七绝\n"
        ret += r"请输入你的底稿，用？代替你想Vena帮你生成的内容，或者输入'go'直接开始"
        return ret

class Poem(models.Model):
    id = models.AutoField(db_column='id', primary_key=True)
    user = models.ForeignKey(User, related_name='poem', on_delete=models.CASCADE)
    content = models.CharField(max_length=512)
    description = models.TextField(blank=True)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.content

    class Meta:
        verbose_name_plural = 'poem'

# Create your models here.
class Tag(models.Model):
    name = models.CharField(verbose_name='标签名', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        verbose_name = '标签名称'  # 指定后台显示模型名称
        verbose_name_plural = '标签列表'  # 指定后台显示模型复数名称
        db_table = "tag"  # 数据库表名


class Category(models.Model):
    name = models.CharField(verbose_name='类别名称', max_length=64)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)

    class Meta:
        ordering = ['name']
        verbose_name = "类别名称"
        verbose_name_plural = '分类列表'
        db_table = "category"  # 数据库表名

    # 使对象在后台显示更友好
    def __str__(self):
        return self.name


class Article(models.Model):
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    title = models.CharField(verbose_name='标题', max_length=100)
    content = models.TextField(verbose_name='正文', blank=True, null=True)
    status = models.CharField(verbose_name='状态', max_length=1, choices=STATUS_CHOICES, default='p')
    views = models.PositiveIntegerField(verbose_name='浏览量', default=0)
    created_time = models.DateTimeField(verbose_name='创建时间', default=now)
    pub_time = models.DateTimeField(verbose_name='发布时间', blank=True, null=True)
    last_mod_time = models.DateTimeField(verbose_name='修改时间', default=now)
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE, blank=False, null=False)
    tags = models.ManyToManyField(Tag, verbose_name='标签集合', blank=True)

    # 使对象在后台显示更友好
    def __str__(self):
        return self.title

    # 更新浏览量
    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])

    # 下一篇
    def next_article(self):  # id比当前id大，状态为已发布，发布时间不为空
        return Article.objects.filter(id__gt=self.id, status='p', pub_time__isnull=False).first()

    # 前一篇
    def prev_article(self):  # id比当前id小，状态为已发布，发布时间不为空
        return Article.objects.filter(id__lt=self.id, status='p', pub_time__isnull=False).first()

    class Meta:
        ordering = ['-pub_time']  # 按文章创建日期降序
        verbose_name = '文章'  # 指定后台显示模型名称
        verbose_name_plural = '文章列表'  # 指定后台显示模型复数名称
        db_table = 'article'  # 数据库表名
        get_latest_by = 'created_time'

class Image(models.Model):
    # upload_to 表示图像保存路径
    img = models.ImageField(upload_to = 'image')
    name = models.CharField(max_length = 50)
    description = models.TextField(blank=True)
    created_time = models.DateTimeField(verbose_name='create_time', default=now)

    class Meta:
        db_table = "image"

    def __str__(self):
        return self.name





