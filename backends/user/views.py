import re
from django.contrib.auth import login,authenticate,logout
from utils.view import LoginRequiredJSONMixin
# Create your views here.
from .models import User,UserModelSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

#检查用户名是否已存在
class usernameCountAPI(APIView):

    def get(self,request,username):


        count = User.objects.filter(username=username).count()
        return Response({'code':0,'count':count,'errmsg':'ok'})

#检查手机号是否已存在
class mobileCountAPI(APIView):
    def get(self,request,mobile):

        count = User.objects.filter(mobile=mobile).count()
        return Response({'code':0,'count':count,'errmsg':'ok'})

#新用户注册API
class registerNewAPI(APIView):
    def post(self,request):
        user=request.data
        username=user.get('username')
        password=user.get('password')
        password2=user.get('password2')
        email=user.get('email')
        mobile=user.get('mobile')
        allow=user.get('allow')

        if not all([username,password,password2,mobile,allow]):
            return Response({'code':400,'errmsg':'Incomplete parameters'})

        if not re.match('[a-zA-Z0-9_-]{5,20}',username):
            return Response({'code':400,'errmsg':'Incorrect user name'})
        
        if not password==password2:
            return Response({'code':400,'errmsg':'Password error'})

        if not re.match('1[345789]\d{9}',mobile):
            return Response({'code':400,'errmsg':'Incorrect mobilephone number'})

        if not 8<=len(password)<=20:
            return Response({'code':400,'errmsg':'Incorrect password length'})

        if not allow:
            return Response({'code':400,'errmsg':'Agreement not agreed'})

        #保存用户注册信息到数据库
        try:
            user_save=User.objects.create_user(username=username,password=password,mobile=mobile,email=email)

            login(request,user_save)
        except Exception as e:
            return Response({'code':400,'errmsg':str(e)})

        return Response({'code':0,'errmsg':'ok'})

#用户登录API
class userloginAPI(APIView):
    def post(self,request):
        data=request.data
        username=data.get('username')
        password=data.get('password')
        remembered=data.get('remembered')

        if not all([username,password]):
            return Response({'code':400,'errmsg':'Incomplete parameters'})

        
        #判断是否是手机号登录
        if re.match('1[345789]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        else:
            User.USERNAME_FIELD='username'
        
        #登录验证
        user=authenticate(username=username,password=password)
        if not user:
            return Response({'code':400,'errmsg':'Incorrect user name or password'})

        
        #是否登录保持
        if remembered:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        
        login(request,user)

        #获取登录用户信息
        a=object()
        if User.USERNAME_FIELD=='mobile':
            a=User.objects.get(mobile=username)
        else:
            a=User.objects.get(username=username)

        #制作响应信息
        response=Response({'code':0,'errmsg':'ok'})
        response.set_cookie('username',a.username)

        return response

#用户退出API
class logoutAPI(APIView):
    def delete(self,request):
        logout(request)

        response=Response({'code':0,'errmsg':'ok'})
        response.delete_cookie('username')

        return response


#用户中心进入API
class centerViewAPI(LoginRequiredJSONMixin,APIView):

    def get(self,request):
        user=request.user
        info=UserModelSerializer(instance=user)


        return Response({'code':0,'errmsg':'ok','info_data':info.data})


#用户修改密码
class passwordChangeAPI(APIView):
    def put(self,request):
        user=request.user
        data = request.data
        old_password=data.get('old_password')
        new_password=data.get('new_password')
        new_cpassword=data.get('new_password2')
        if not user.check_password(old_password):
            return Response({"code":400,"errmsg":"Inconrent password"})
        if new_cpassword!=new_password:
            return Response({"code":400,"errmsg":"Inconrent data"})

        user.set_password(new_password)
        user.save()
        return Response({'code':0,'errmsg':'ok'}).delete_cookie('username')

# name='xiangxin'
# if  not User.objects.filter(username=name):
#     User.objects.create_superuser(username=name,password='lxb331047471a',email='2868308648@qq.com',mobile='15397008301')
# else:
#     User.objects.filter(username=name).delete()
#     User.objects.create_superuser(username=name,password='lxb331047471a',email='2868308648@qq.com',mobile='15397008301')
