from django.db import models

# Create your models here.

from iphone import settings


class ImgBaseInfo(models.Model):
    img_id = models.CharField(max_length=30, unique=True, verbose_name="图片ID")  # 图片ID
    max_id = models.CharField(max_length=30, unique=True, verbose_name="大图ID")
    min_id = models.CharField(max_length=30, unique=True, verbose_name="小图ID")


class ImgInfo(models.Model):
    iid = models.CharField(max_length=30, unique=True, verbose_name="图片ID")  # 图片ID
    created_time = models.DateTimeField(auto_now_add=True, verbose_name='创建时间', )  # 创建时间
    size = models.CharField(max_length=50, verbose_name="图片大小")  # 图片大小
    img_url = models.ImageField(max_length=200, upload_to="serverImg", verbose_name="图片路径")  # 图片存储路径

    def image_tag(self):
        return u'<img src="%sserverImg/%s" />' % (settings.MEDIA_URL, self.img_url)

    image_tag.allow_tags = True
    image_tag.short_description = "图片"

    class Meta:
        verbose_name_plural = '图片'
        verbose_name = '图片'
        ordering = ['-created_time']
