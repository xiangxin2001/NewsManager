# Generated by Django 4.0.3 on 2023-03-27 07:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_usercharacters'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usercharacters',
            name='news_categroy',
        ),
        migrations.AddField(
            model_name='usercharacters',
            name='news_categroy_interested',
            field=models.TextField(blank=True, null=True, verbose_name='用户感兴趣新闻类别信息'),
        ),
        migrations.AddField(
            model_name='usercharacters',
            name='similar_users',
            field=models.TextField(blank=True, null=True, verbose_name='相似用户'),
        ),
    ]