import re
from django.contrib.auth import login,authenticate,logout
from utils.view import LoginRequiredJSONMixin
# Create your views here.
from .models import User,UserModelSerializer,UserCharacters
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
#检查邮箱是否已存在
class emailCountAPI(APIView):
    def get(self,request,email):
        count = User.objects.filter(email=email).count()
        return Response({'code':0,'count':count,'errmsg':'ok'})

#新用户注册API
class registerNewAPI(APIView):
    def post(self,request):
        user=request.data
        username=user.get('username')
        password=user.get('password')
        checkPassword=user.get('checkPassword')
        email=user.get('email')
        mobile=user.get('mobile')
        allow=user.get('allow')

        if not all([username,password,checkPassword,mobile,allow,email]):
            print([username,password,checkPassword,mobile,allow,email])
            return Response({'code':400,'errmsg':'Incomplete parameters'})

        if not 1<=len(username)<=20:
            return Response({'code':400,'errmsg':'Incorrect username length'})
        
        if not password==checkPassword:
            return Response({'code':400,'errmsg':'Password error'})

        if not re.match('1[345789]\d{9}',mobile):
            return Response({'code':400,'errmsg':'Incorrect mobilephone number'})

        if not 6<=len(password)<=20:
            return Response({'code':400,'errmsg':'Incorrect password length'})

        if not allow:
            return Response({'code':400,'errmsg':'Agreement not agreed'})

        #保存用户注册信息到数据库
        try:
           user_obj=User.objects.create_user(username=username,password=password,mobile=mobile,email=email)
           UserCharacters.objects.create(user=user_obj)
           user_obj.save()
        except Exception as e:
            return Response({'code':400,'errmsg':str(e)})

        return Response({'code':0,'errmsg':'ok'})

#用户登录API
class userloginAPI(APIView):
    def post(self,request):
        data=request.data
        username=data.get('username')
        password=data.get('password')
        remember=data.get('remember')

        if not all([username,password]):
            return Response({'code':400,'errmsg':'Incomplete parameters'})

        
        #判断登录方式
        if re.match(r'1[345789]\d{9}',username):
            User.USERNAME_FIELD='mobile'
        elif re.match(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$',username):
            User.USERNAME_FIELD='email'
        else:
            User.USERNAME_FIELD='username'
        
        #登录验证
        user=authenticate(username=username,password=password)
        if not user:
            return Response({'code':400,'errmsg':'Incorrect user name or password'})

        
        #是否登录保持
        if remember:
            request.session.set_expiry(None)
        else:
            request.session.set_expiry(0)
        
        login(request,user)

        #获取登录用户信息
        a=object()
        if User.USERNAME_FIELD=='mobile':
            a=User.objects.get(mobile=username)
        elif User.USERNAME_FIELD=='email':
            a=User.objects.get(email=username)
        else:
            a=User.objects.get(username=username)

        #补创用户特征
        if not UserCharacters.objects.filter(user=a):
            UserCharacters.objects.create(user=a)
        #制作响应信息
        response=Response({'code':0,'errmsg':'ok','session_id':request.session,'username':a.username})
        username=a.username.encode(encoding='utf-8')
        response.set_cookie('username',username,samesite="None",secure=True)

        return response
    #获取用户登录状态
    def get(self,request):
        try:
            user=request.user
            if user.username=="AnonymousUser":
                return Response({'code':400,'errmsg':'AnonymousUser','logined':False})
            if User.objects.get(username=user.username):
                return Response({'code':0,'erermsg':'ok','logined':True,'username':user.username})
            else:
                return Response({'code':400,'errmsg':'AnonymousUser','logined':False})
        except Exception as e:
            print(e)
            return Response({'code':400,'errmsg':e,'logined':False})


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

# name='秋沐川'
# if  not User.objects.filter(username=name):
#     User.objects.create_superuser(username=name,password='lxb331047471a',email='2868308648@qq.com',mobile='15397008302')
# else:
#     User.objects.filter(username=name).delete()
#     User.objects.create_superuser(username=name,password='lxb331047471a',email='2868308648@qq.com',mobile='15397008302')
import json
from news.models import News,NewsCharacters,Category
from jieba import analyse
import math
class UserPoiCalculate:
    def __init__(self,user:object) -> None:
        self.flag=True
        try:
            self.usercharacters=UserCharacters.objects.get(user=user)
        except Exception as e:
            self.flag=False
            print('用户{}角色特征不存在，请检查'.format(user.username))
    #根据浏览历史计算新闻关键词
    def calculate_news_keyword(self)->None:
        if self.flag:
            news_history=json.loads(self.usercharacters.news_history)
            keywords=''''''
            for news_id,num_visited in news_history.items():
                try:
                    newscharacters=NewsCharacters.objects.get(news=news_id)
                    keywords=keywords+','+newscharacters.keywords*int(num_visited)
                except Exception as e:
                    print(e)
            keyword_list=analyse.extract_tags(keywords,topK=30, withWeight=False, allowPOS=('n','v','nr','a','ns','s','nt','ORG','PER','LOC','nw'))
            keywords=','.join(keyword_list)
            self.usercharacters.news_keyword=keywords
            self.usercharacters.save()
            
    #根据浏览历史计算新闻种类偏好
    def calculate_Poi(self)->None:
        if self.flag:
            category_count={}
            for category in Category.objects.all():
                category_count[category.id]={'total':int(category.newsnum),'count':0,'grade':0}
            
            news_history=json.loads(self.usercharacters.news_history)
            total_visited=0
            for news_id,num_visited in news_history.items():
                try:
                    news_category=News.objects.get(id=news_id).category.id
                    category_count[news_category]['count']+=int(num_visited)
                    total_visited+=int(num_visited)
                except Exception as e:
                    print(e)
            for category in category_count.keys():
                category_count[category]['grade']=int(10*(category_count[category]['count']/category_count[category]['total']))+int(90*(category_count[category]['count']/total_visited))
            self.usercharacters.news_categroy_Poi=json.dumps(category_count)
            self.usercharacters.save()

    #根据新闻种类偏好计算类似用户    
    def calculate_similar_users(self)->None:
        similar_users={'similar':[],'differ':[]}
        try:
            news_categroy_Poi_me=json.loads(self.usercharacters.news_categroy_Poi)
            for a_usercharacters in UserCharacters.objects.all():
                cosine_similarity_part1,cosine_similarity_part2,cosine_similarity_part3=0,0,0
                news_categroy_Poi_other=json.loads(a_usercharacters.news_categroy_Poi)
                for category in Category.objects.all():
                    category_id=str(category.id)
                    cosine_similarity_part1+=news_categroy_Poi_me[category_id]['grade']*news_categroy_Poi_other[category_id]['grade']
                    cosine_similarity_part2+=news_categroy_Poi_me[category_id]['grade']*news_categroy_Poi_me[category_id]['grade']
                    cosine_similarity_part3+=news_categroy_Poi_other[category_id]['grade']*news_categroy_Poi_other[category_id]['grade']
                cosine_similarity=cosine_similarity_part1/(math.pow(cosine_similarity_part2,0.5)*math.pow(cosine_similarity_part3,0.5))
                if cosine_similarity>0.6:
                    similar_users['similar'].append(str(a_usercharacters.user.uid))
                elif cosine_similarity<-0.4:
                    similar_users['differ'].append(str(a_usercharacters.user.uid))
            print("kkkalsd")
            self.usercharacters.similar_users=json.dumps(similar_users)
            self.usercharacters.save()
        except Exception as e:
            print(e)


#入口，启动用户特征的计算
def calculate_usercharacters():
    for user in User.objects.all():
        try:
            upc=UserPoiCalculate(user=user)
            upc.calculate_news_keyword()
            upc.calculate_Poi()
            import time
            time.sleep(1)
            upc.calculate_similar_users()
            print('{}的用户模型已计算成功'.format(user.username))
        except Exception as e:
            print('{},错误:{}'.format(user.username,str(e))) 

