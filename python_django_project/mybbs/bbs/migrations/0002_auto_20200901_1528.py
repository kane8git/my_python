# Generated by Django 3.1 on 2020-09-01 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bbs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='head_img',
            field=models.ImageField(default=0, upload_to='', verbose_name='文章标题图片'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='comment',
            name='comment_type',
            field=models.IntegerField(choices=[(1, '评论'), (2, '点赞')], default=1),
        ),
    ]
