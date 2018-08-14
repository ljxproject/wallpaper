import time
from django.shortcuts import render
from rest_framework import serializers
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.core.paginator import Paginator

from .models import ImgBaseInfo


# Create your views here.


class ImgListSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        current_page = data.get("current_page")
        next_page = data.get("next_page")
        box_list = []
        for i in data.get("list_data"):
            box = {"imageID": i}
            box_list.append(box)
        return {
            "ListData": box_list,
            "CurrentPage": current_page,
            "NextPage": next_page
        }


@api_view(["GET"])
def img_list(request):
    img_base_list = ImgBaseInfo.objects.all()[::-1]
    list_data = []
    p = Paginator(img_base_list, 20)
    max_page = p.num_pages
    cp_num = int(request.GET.get("currentPage")) if request.GET.get("currentPage") else None
    if not cp_num:
        objs = p.page(1)
    elif cp_num > max_page:
        objs = p.page(max_page)
    else:
        objs = p.page(cp_num)
    for i in list(objs):
        img_id = i.img_id
        list_data.append(img_id)
    if not cp_num:
        current_page = 1
    else:
        if cp_num >= max_page:
            current_page = max_page
        else:
            current_page = cp_num
    if not cp_num:
        next_page = 2
    else:
        if cp_num >= max_page:
            next_page = max_page
        else:
            next_page = cp_num + 1
    data = {"list_data": list_data,
            "current_page": current_page,
            "next_page": next_page}
    serializer = ImgListSerializer(data)
    return Response(serializer.data)


class TimeSerializer(serializers.BaseSerializer):

    def to_representation(self, data):
        return {
            "gmt_time": data.get("gmt_time")
        }


@api_view(["GET"])
def get_time(request):
    data = {
        "gmt_time": time.time()}
    serializers = TimeSerializer(data)
    return Response(serializers.data)
