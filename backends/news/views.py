import pytz
from utils.sprider.sprider import main,BASE_DIR
from .models import News,Category,NewsCharacters
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas
import datetime
from user.models import UserCharacters,User
# Create your views here.
#爬取的新闻入库
def Sprider_data_in():
    DEBUG=False
    sp=main()
    sp.main()
    target_list={}
    import json
    with open(BASE_DIR/"target.json","r",encoding="utf-8") as f:
        target_list=json.load(f)
        target_list=target_list["target_list"]
    if target_list:
        count=0
        for target in target_list:
            data_dict=pandas.read_csv(BASE_DIR/'{}.csv'.format(target["name"]),index_col=0, squeeze=True).to_dict()
            for i in data_dict['title'].keys():
                if not News.objects.filter(title=data_dict['title'][i]) and data_dict['passage'][i] !="nan" :
                    news_obj=News.objects.create(title=data_dict['title'][i],category=Category.objects.get(id=data_dict['category'][i]),passage=data_dict['passage'][i],news_from=data_dict['news_from'][i],url=data_dict['url'][i])
                    #新入库的新闻特征建模
                    news_str=news_obj.title+news_obj.passage
                    news_str=news_str.replace(r'<(\S*?)[^>]*>.*?|<.*? />','')
                    keyword_list=analyse.extract_tags(news_str,topK=20, withWeight=False, allowPOS=('n','v','nr','a','ns','s','nt','ORG','PER','LOC','nw'))
                    keywords=','.join(keyword_list)
                    NewsCharacters.objects.create(news=news_obj,keywords=keywords)
                    news_obj.save()
                    if DEBUG:
                        print("新闻{}入库，特征已创建".format(data_dict['title'][i]))
                    
                else:
                    if DEBUG:
                        print("数据重复")
                if not DEBUG:
                    total=len(target_list)
                    barlen=30
                    print('\r{}[{}]{}/{}'.format('新闻数据入库', '*'*(count*barlen//total)+'-'*(barlen-count*barlen//total),count,total),end='')
            count+=1
            
        News.objects.filter(passage='nan').delete()
        #计算各种类的新闻数量
        for category in Category.objects.all():
            category.newsnum=News.objects.filter(category=category).count()
            category.save()

        print("\n新闻获取成功") 



# Sprider_data_in()

# test=News.objects.get(title="春来水暖鸟先知")
# print(test.passage)
#新闻详情获取API
import json
class News_detailAPI(APIView):
    def get(self,request,news_id):
        news_id=int(news_id)
        try:
            news=News.objects.get(id=news_id)
            if news:
                newsc=NewsCharacters.objects.get(news=news)
                newsc.visited+=1
                newsc.save()
                try:
                    if User.objects.get(username=request.user.username):
                        usercharacters=UserCharacters.objects.get(user=User.objects.get(username=request.user.username))
                        if usercharacters.news_history:
                            news_history=json.loads(usercharacters.news_history)
                        else:
                            news_history={}
                        news_id=str(news_id)
                        if news_id in news_history:
                            news_history[news_id]+=1
                        else:
                            news_history[news_id]=1
                        usercharacters.news_history=json.dumps(news_history)
                        usercharacters.save()
                except Exception as e:
                    print(e)
                news_info={
                    "title":news.title,
                    "category":str(news.category.id),
                    "passage":str(news.passage),
                    "news_from":news.news_from,
                    "url":news.url,
                    "visited":newsc.visited,
                    "breadcrumb":{"首页":"/",str(news.category.name):"/category/{}".format(news.category.id),news.title:"/detail/{}".format(news_id)},
                    "visited":str(newsc.visited)
                }

                return Response({"code":0,"errmsg":"ok","news":news_info})
            else:
                return Response({"code":500,"errmsg":"newsDoNotExist"})
        except Exception as e:
            print(e)
            return Response({"code":500,"errmsg":str(e)})

class News_categoryAPI(APIView):
    def get(self,request,category_id):
        category_id=int(category_id)
        try:
            page=int(request.GET.get('page',1))
            pagesize=int(request.GET.get('pagesize',15))
            news_list=News.objects.filter(category=category_id).order_by("-create_time")
            total=len(news_list)
            news_list_list=[]
            if total>1:
                if total>=page*pagesize:
                    news_list=news_list[pagesize*(page-1):pagesize*page]
                else:
                    news_list=news_list[pagesize*(page-1):total]
                for news in news_list:
                    time=(news.create_time+datetime.timedelta(hours=8)).strftime(r"%Y-%m-%d")
                    time=time.split('-')
                    timestr="{}年{}月{}日".format(time[0],time[1],time[2])
                    news_info={
                        "title":news.title,
                        "url":"/detail/{}".format(news.id),
                        "time":timestr
                    }
                    news_list_list.append(news_info)
                bread={"首页":"/",str(Category.objects.get(id=category_id).name):"/category/{}".format(category_id),
                       "第{}页".format(page):"/category/{}?page={}&pagesize={}".format(category_id,page,pagesize)}
                return Response({"code":0,"errmsg":"ok","total":total,"news_list":news_list_list, "breadcrumb":bread})
            else:
                return Response({"code":500,"errmsg":"categoryDoNotExist"})
        except Exception as e:
            return Response({"code":500,"errmsg":str(e)})

#新闻搜索API
from haystack.views import SearchView
from django.http import JsonResponse
from operator import attrgetter
class NewsSearchView(SearchView):
     def create_response(self):
        context = self.get_context()
        news_list=[]
        obj_list=[]
        for news in context['page'].object_list:
            try:
                id=str(news.id)
                id=id.split('.')
                id=id[-1]
                news_obj=News.objects.get(id=id)
                obj_list.append(news_obj)
            except Exception as e:
                print(e)
        obj_list.sort(reverse=True,key=attrgetter("create_time"))
        for news_obj in obj_list:
            try:
                time=(news_obj.create_time).strftime(r"%Y-%m-%d")
                time=time.split('-')
                timestr="{}年{}月{}日".format(time[0],time[1],time[2])
                news_list.append({
                    "title":news_obj.title,
                    "url":"/detail/{}".format(news_obj.id),
                    "time":timestr,
                })
            except Exception as e:
                print(e)
           
        result_json={
            'code':0,
            'errmsg':'ok',
            'searchkey': context.get('query'),
            'page_size': context['page'].paginator.num_pages,
            'count': context['page'].paginator.count,
            'news_list':news_list,
        }
     
        return JsonResponse(result_json,safe=False)
     
from jieba import analyse
#已有新闻特征建模函数
def NewsCharacterforowned():
    news_list=News.objects.all()
    for news in news_list:
        if not NewsCharacters.objects.get(news=news):
            news_str=news.title+news.passage
            news_str=news_str.replace(r'<(\S*?)[^>]*>.*?|<.*? />','')
            keyword_list=analyse.extract_tags(news_str,topK=20, withWeight=False, allowPOS=('n','v','nr','a','ns','s','nt','ORG','PER','LOC','nw'))
            keywords=','.join(keyword_list)
            NewsCharacters.objects.create(news=news,keywords=keywords)

#获取最新新闻
class LatestNewsAPI(APIView):
    def get(self,request):
        try:
            category=Category.objects.all()
            category_dict={}
            news_dict={}
            for cat in category:
                category_dict[cat.id]=cat.name
                try:
                    news_list=News.objects.filter(category=cat.id).order_by("-create_time")[:10]
                    latest_news_list=[]
                    for news in news_list:
                        latest_news_list.append({
                            "title":news.title,
                            "url":"/detail/{}".format(news.id),
                            })
                except Exception as e:
                    print(e)
                    latest_news_list=[]
                news_dict[cat.id]=latest_news_list
            return Response({"code":0,"errmsg":'ok','latest_news':news_dict,'category':category_dict})
        except Exception as e:
            return Response({"code":500,"errmsg":str(e)})

#获取热点新闻

class HotNewsAPI(APIView):
    def get(self,request):
        try:
            hot_news=[]
            newsc_list=NewsCharacters.objects.filter(news__create_time__gt=datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-datetime.timedelta(days=3)).order_by('-visited','-news__create_time')[:20]
            for newsc in newsc_list:
                hot_news.append({
                    "title":newsc.news.title,
                    "url":"/detail/{}".format(newsc.news.id),
                    })
            return Response({"code":0,"errmsg":'ok','hot_news':hot_news})
        except Exception as e:
            return Response({"code":500,"errmsg":str(e)})

#个性化推荐(一次20条)
from django_redis import get_redis_connection
class PersonalizeNewsAPI(APIView):
    def mySerializer(self,news)->dict:
        time=(news.create_time+datetime.timedelta(hours=8)).strftime(r"%Y-%m-%d")
        time=time.split('-')
        timestr="{}年{}月{}日".format(time[0],time[1],time[2])
        return{
                "title":news.title,
                "url":"/detail/{}".format(news.id),
                "time":timestr
                }
    def get(self,request):
        try:
            personalize_news_list=[]
            personalize_news_caches=get_redis_connection('personalize_news_caches')
            pushed_news_list=[]
            try:
                if personalize_news_caches.get(request.user.username)=='nil' or personalize_news_caches.get(request.user.username)==None:
                    personalize_news_caches.set(request.user.username,','.join(pushed_news_list),3600)
                else:
                    pushed_news_list=personalize_news_caches.get(request.user.username).decode('utf-8').split(',')
            except:
                personalize_news_caches.set(request.user.username,','.join(pushed_news_list),3600)
            
            usercharacters=UserCharacters.objects.get(user=request.user)
            news_history_dict=json.loads(usercharacters.news_history)
            #40%相似用户推荐
            try:
                count=0
                similar_users_dict=json.loads(usercharacters.similar_users)
                for uid in similar_users_dict['similar']:
                    if count<24:
                        similar_userc=UserCharacters.objects.get(user=uid)
                        similar_user_news_history_dict=json.loads(similar_userc.news_history)
                        for news_id in similar_user_news_history_dict:
                            
                            if count<24:
                                if str(news_id) not in pushed_news_list :
                                    if News.objects.get(id=news_id).create_time >= datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-datetime.timedelta(days=30):
                                        pushed_news_list.append(str(news_id))
                                        personalize_news_list.append(self.mySerializer(news=News.objects.get(id=news_id)))
                                        count+=1
                                        
                            else:
                                break
            except Exception as e:
                print(e)
            #50%关键词推荐
            try:
                count=0
                news_keyword_list=usercharacters.news_history.split(',')
                for a_newsc in NewsCharacters.objects.filter(news__create_time__gt=datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-datetime.timedelta(days=7)).order_by('-news__create_time'):
                    if count<30:
                        if str(a_newsc.news.id) not in pushed_news_list:
                            intersection=set(news_keyword_list).intersection(set(a_newsc.keywords.split(',')))
                            # print(len(intersection))
                            # print(intersection)
                            if len(intersection) >=1:
                                pushed_news_list.append(str(a_newsc.news.id))
                                personalize_news_list.append(self.mySerializer(news=a_newsc.news))
                                count+=1
                    else:
                        break
                if count<30:
                   news_categroy_Poi=json.loads(usercharacters.news_categroy_Poi)
                   leave=30-count
                   for category_id in news_categroy_Poi.keys():
                        count=0
                        if count<int(leave*float(news_categroy_Poi[category_id]['percentage'])):
                            for a_news in News.objects.filter(category=category_id,create_time__gt=datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-datetime.timedelta(days=30)).order_by('-create_time'):
                                if count<int(leave*float(news_categroy_Poi[category_id]['percentage'])):
                                    if str(news_id) not in pushed_news_list :
                                        count+=1
                                        pushed_news_list.append(str(a_news.id))
                                        personalize_news_list.append(self.mySerializer(news=a_news))
                                else:
                                    break
                import random
                if len(personalize_news_list)<54:
                    for news_id in pushed_news_list:
                        if random.randint(0,10)<4 and len(personalize_news_list)<54:
                            personalize_news_list.append(self.mySerializer(news=News.objects.get(id=news_id)))
            except Exception as e:
                print(e)
            #10%试探性推荐
            try:
                count=0
                similar_users_dict=json.loads(usercharacters.similar_users)
                for uid in similar_users_dict['differ']:
                    if count<6:
                        differ_userc=UserCharacters.objects.get(user=uid)
                        differ_user_news_history_dict=json.loads(differ_userc.news_history)
                        for news_id in differ_user_news_history_dict:
                            if count<6:
                                if str(news_id) not in pushed_news_list and news_id not in news_history_dict:
                                    if News.objects.get(id=news_id).create_time >= datetime.datetime.now().replace(tzinfo=pytz.timezone('UTC'))-datetime.timedelta(days=30):
                                        pushed_news_list.append(str(news_id))
                                        personalize_news_list.append(self.mySerializer(news=News.objects.get(id=news_id)))
                                        count+=1
                            else:
                                break
            except Exception as e:
                print(e)

            personalize_news_caches.set(request.user.username,','.join(pushed_news_list))
            return Response({"code":0,"errmsg":'ok','personalize_news_list':personalize_news_list})
        except Exception as e:
            return Response({"code":500,"errmsg":str(e)})
        

