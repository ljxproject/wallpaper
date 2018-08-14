import os
import gzip

from PIL import Image
from django.contrib import admin, messages

from app.helps.imgname import createImg
from app.helps.pngtojpg import pngToJpg
from app.helps.thumbnail import toSmall
from iphone import settings
from .models import ImgInfo, ImgBaseInfo


# Register your models here.
class ImgIdListFilter(admin.SimpleListFilter):
    title = (u"图片类型")
    parameter_name = "iid"

    def lookups(self, request, model_admin):
        return (("small", u"小图",),
                ("big", u"大图",),)

    def queryset(self, request, queryset):
        if self.value() == "small":
            return queryset.filter(iid__contains="s")
        if self.value() == "big":
            return queryset.filter(iid__contains="p")


class ImgInfoAdmin(admin.ModelAdmin):
    list_display = ['iid', 'img_url', 'image_tag', 'created_time', 'size']
    fields = ['img_url']
    list_per_page = 10
    list_filter = [ImgIdListFilter]

    def save_model(self, request, obj, form, change):
        # 获取图片及图片名
        img = form.cleaned_data.get("img_url")
        # 验证上传图片是否为png或jpg
        type_list = [".jpg", ".png"]
        # 前缀
        prefix = createImg(4)
        # 后缀
        suffix = os.path.splitext(img.name)[1]
        # 打开图片
        img = Image.open(img)
        if not suffix.lower() in type_list:
            self.message_user(request, u"上传图片格式不正确", messages.ERROR)
        else:
            # 如果是png则转换
            if suffix.lower() == ".png":
                img = pngToJpg(img)
            # 获取图片ID&拼接图片ID(p)
            iid_p = prefix + "p"
            # 检验图片是否存在
            if ImgInfo.objects.filter(iid=iid_p):
                self.message_user(request, u"图片已存在", messages.ERROR)
            # 更改图片名字为图片IDp.jpg,保存路径
            filename = iid_p + ".jpg"
            pathname = os.path.join(settings.MEDIA_ROOT,  "serverImg/" + filename)
            img.save(pathname)
            # 压缩图片并保持
            img_file = open(pathname, 'rb')
            img_gzip = gzip.open(pathname + '.gz', 'wb', compresslevel=9)
            img_gzip.writelines(img_file)
            img_gzip.close()

            # 计算图片大小
            size = str("%.3fM" % (os.path.getsize(pathname) / (1024 * 1024)))
            # request ={img_id(new),img_url(new)}   ImgBase.save()
            ii_obj = ImgInfo(iid=iid_p, img_url=filename, size=size)
            ii_obj.save()

            # 拼接图片ID(s)
            iid_s = prefix + "s"
            # 检验图片是否存在
            if ImgInfo.objects.filter(iid=iid_s):
                self.message_user(request, u"图片已存在", messages.ERROR)
            # 对图片进行缩略
            img = toSmall(img)
            # 更改图片名字为图片IDs.jpg,保存路径
            filename = iid_s + ".jpg"
            pathname = os.path.join(settings.MEDIA_ROOT, "serverImg/" + filename)
            img.save(pathname)
            # 计算图片大小
            size = str("%.3fM" % (os.path.getsize(pathname) / (1024 * 1024)))
            # ImgInfo.save()
            ii_obj = ImgInfo(iid=iid_s, img_url=filename, size=size)
            ii_obj.save()
            # ImgBaseInfo.save()
            ii_obj = ImgBaseInfo(img_id=prefix, max_id=iid_p, min_id=iid_s)
            ii_obj.save()


admin.site.register(ImgInfo, ImgInfoAdmin)
