# Generated by Django 4.0.3 on 2023-02-15 08:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('name', models.CharField(max_length=40, verbose_name='名称')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='subs', to='news.category', verbose_name='上级类别')),
            ],
            options={
                'verbose_name': '类别',
                'verbose_name_plural': '类别',
                'db_table': 'tb_category',
            },
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='创建时间')),
                ('update_time', models.DateTimeField(auto_now=True, verbose_name='更新时间')),
                ('title', models.CharField(max_length=200, verbose_name='标题')),
                ('passage', models.TextField(verbose_name='正文')),
                ('news_from', models.CharField(default='互联网', max_length=100, verbose_name='新闻来源')),
                ('url', models.CharField(max_length=100, verbose_name='新闻来源url')),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='news_category', to='news.category', verbose_name='类别')),
            ],
            options={
                'verbose_name': '新闻',
                'verbose_name_plural': '新闻',
                'db_table': 'tb_news',
            },
        ),
    ]
