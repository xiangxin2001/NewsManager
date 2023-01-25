from django.db import models
from utils.models import BaseModel
# Create your models here.
class News(BaseModel):
    title=models.CharField(max_length=200,verbose_name="标题")
    category=models.ForeignKey('Category',on_delete=models.PROTECT,related_name='news_category')
    passage=models.TextField(verbose_name="正文")
    class Meta:
        db_table = 'tb_news'
        verbose_name = '新闻'
        verbose_name_plural = verbose_name

class Categroy(BaseModel):
    name = models.CharField(max_length=40,verbose_name='名称')
    parent = models.ForeignKey('self',on_delete=models.SET_NULL,related_name='subs',null=True,blank=True,verbose_name='上级类别')
    class Meta:
        db_table='tb_category'
        verbose_name='类别'
        verbose_name_plural=verbose_name
