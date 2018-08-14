import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iphone.settings")
django.setup()
from PIL import Image
from app.helps.imgname import createImg
from app.helps.pngtojpg import pngToJpg
from app.helps.thumbnail import toSmall
from app.models import ImgInfo, ImgBaseInfo
from iphone import settings



def imgUpLoad(path):
    file_name_list = os.listdir(path)
    for file_name in file_name_list:
        print(file_name)
        img = os.path.join(path, file_name)
        # 验证上传图片是否为png或jpg
        type_list = [".jpg", ".png"]
        # 前缀
        prefix = createImg(5)
        # 后缀
        suffix = os.path.splitext(file_name)[1]
        # 打开图片
        img = Image.open(img)
        if not suffix.lower() in type_list:
            raise ValueError(u"上传图片格式不正确")
        else:
            # 如果是png则转换
            if suffix.lower() == ".png":
                img = pngToJpg(img)
            # 获取图片ID&拼接图片ID(p)
            iid_p = prefix + "p"
            # 检验图片是否存在
            if ImgInfo.objects.filter(iid=iid_p):
                raise ValueError(u"图片已存在")
            # 更改图片名字为图片IDp.jpg,保存路径
            filename = "serverImg/" + iid_p + ".jpg"
            pathname = os.path.join(settings.MEDIA_ROOT, filename)
            img.save(pathname)
            # 计算图片大小
            size = str("%.3fM" % (os.path.getsize(pathname) / (1024 * 1024)))
            # request ={img_id(new),img_url(new)}   ImgBase.save()
            ii_obj = ImgInfo(iid=iid_p, img_url=filename, size=size)
            ii_obj.save()

            # 拼接图片ID(s)
            iid_s = prefix + "s"
            # 检验图片是否存在
            if ImgInfo.objects.filter(iid=iid_s):
                raise ValueError(u"图片已存在")
            # 对图片进行缩略
            img = toSmall(img)
            # 更改图片名字为图片IDs.jpg,保存路径
            filename = "serverImg/" + iid_s + ".jpg"
            pathname = os.path.join(settings.MEDIA_ROOT, filename)
            img.save(pathname)
            # 计算图片大小
            size = str("%.3fM" % (os.path.getsize(pathname) / (1024 * 1024)))
            # ImgInfo.save()
            ii_obj = ImgInfo(iid=iid_s, img_url=filename, size=size)
            ii_obj.save()
            # ImgBaseInfo.save()
            ii_obj = ImgBaseInfo(img_id=prefix, max_id=iid_p, min_id=iid_s)
            ii_obj.save()
    print("已成功导入%s张图片" % len(file_name_list))

if __name__ == '__main__':
    imgUpLoad(input("请输入图片上传路径:"))
