# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-06-06 03:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ImgBaseInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img_id', models.CharField(max_length=30, unique=True, verbose_name='图片ID')),
                ('max_id', models.CharField(max_length=30, unique=True, verbose_name='大图ID')),
                ('min_id', models.CharField(max_length=30, unique=True, verbose_name='小图ID')),
            ],
        ),
        migrations.CreateModel(
            name='ImgInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('iid', models.CharField(max_length=30, unique=True, verbose_name='图片ID')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('size', models.CharField(max_length=50, verbose_name='图片大小')),
                ('img_url', models.ImageField(max_length=200, upload_to='serverImg', verbose_name='图片路径')),
            ],
            options={
                'verbose_name': '图片',
                'verbose_name_plural': '图片',
                'ordering': ['-created_time'],
            },
        ),
    ]
