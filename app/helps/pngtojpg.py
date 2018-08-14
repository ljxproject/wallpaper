from PIL import Image


def pngToJpg(img):
    jpg = Image.new("RGB", img.size, (255, 255, 255))
    jpg.paste(img)
    return jpg
