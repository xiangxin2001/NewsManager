from django.db import models
from rest_framework.serializers import ModelSerializer
# Create your models here.
from django.contrib.auth.models import AbstractUser,BaseUserManager
import uuid
class Usermanager(BaseUserManager):
    def create_user(self,username,email,mobile,password):
        if not email:
            raise ValueError('用户创建必须给出邮箱地址')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            mobile=mobile
    
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    def create_superuser(self,username,email,mobile,password):
        if not email:
            raise ValueError('用户创建必须给出邮箱地址')
        
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            mobile=mobile
    
        )
        user.set_password(password)
        user.is_superuser=True
        user.is_staff=True
        user.save(using=self._db)
        return user

#用户模型类
class User(AbstractUser):
    uid=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True)
    mobile=models.CharField(max_length=11,unique=True)
    objects=Usermanager()
    class Meta:
        db_table = 'tb_users'
        verbose_name='用户'
        verbose_name_plural=verbose_name

    def __str__(self)->str:
        return "uid={},username={},is_superuser={},mobile={}".format(self.uid,self.username,self.is_superuser,self.mobile)


class UserModelSerializer(ModelSerializer):

    class Meta:
        model=User
        fields='__all__'

#用户管理模型类


#用户模型的外键使用
# class Grade(models.Model):
#     from backends import settings
#     owner=models.ForeignKey(
#                             settings.AUTH_USER_MODEL,
#                             on_delete=models.CASCADE,
#                             verbose_name='用户'
#                             )
from utils.models import BaseModel
class UserCharacters(BaseModel):
    user=models.ForeignKey('User',on_delete=models.CASCADE,verbose_name='用户')
    news_categroy=models.CharField(max_length=50,blank=True,null=True,verbose_name='用户浏览新闻类别')
    news_keyword=models.CharField(max_length=200,blank=True,null=True,verbose_name='用户浏览新闻关键词')
    news_histroy=models.TextField(blank=True,null=True,verbose_name='用户浏览新闻记录')
    class Meta:
        db_table = 'tb_usercharacters'
        verbose_name='用户特征'
        verbose_name_plural=verbose_name