# Generated by Django 4.0.3 on 2023-03-31 05:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0004_alter_newscharacters_keywords'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='newsnum',
            field=models.IntegerField(blank=True, null=True, verbose_name='新闻数量'),
        ),
    ]