from utils.sprider.sprider import main,BASE_DIR
from .models import News,Category,NewsCharacters
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas

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
                return Response({"code":400,"errmsg":"newsDoNotExist"})
        except Exception as e:
            print(e)
            return Response({"code":400,"errmsg":str(e)})

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
                    time=news.create_time.strftime(r"%Y-%m-%d")
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
                return Response({"code":400,"errmsg":"categoryDoNotExist"})
        except Exception as e:
            print(e)
            return Response({"code":400,"errmsg":str(e)})

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
                time=news_obj.create_time.strftime(r"%Y-%m-%d")
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



