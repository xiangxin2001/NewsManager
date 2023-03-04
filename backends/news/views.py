from utils.sprider.sprider import main,BASE_DIR
from .models import News,Category
from rest_framework.views import APIView
from rest_framework.response import Response
import pandas
# Create your views here.
#爬取的新闻入库
def Sprider_data_in():
    sp=main()
    sp.main()
    target_list={}
    import json
    with open(BASE_DIR/"target.json","r",encoding="utf-8") as f:
        target_list=json.load(f)
        target_list=target_list["target_list"]
    if target_list:
        for target in target_list:
            data_dict=pandas.read_csv(BASE_DIR/'{}.csv'.format(target["name"]),index_col=0, squeeze=True).to_dict()
            for i in data_dict['title'].keys():
                if not News.objects.filter(title=data_dict['title'][i]) and data_dict['passage'][i] !="nan" :
                    News.objects.create(title=data_dict['title'][i],category=Category.objects.get(id=data_dict['category'][i]),passage=data_dict['passage'][i],news_from=data_dict['news_from'][i],url=data_dict['url'][i])
                    print("新闻{}入库".format(data_dict['title'][i]))
                    
                else:
                    print("数据重复")
        News.objects.filter(passage='nan').delete()


# Sprider_data_in()

# test=News.objects.get(title="春来水暖鸟先知")
# print(test.passage)
#新闻详情获取API

class News_detailAPI(APIView):
    def get(self,request,news_id):
        news_id=int(news_id)
        try:
            news=News.objects.get(id=news_id)
            if news:
                news_info={
                    "title":news.title,
                    "categroy":str(news.category.id),
                    "passage":str(news.passage),
                    "news_from":news.news_from,
                    "url":news.url,
                    "breadcrumb":{"首页":"/",str(news.category.name):"/categroy/{}".format(news.category.id),news.title:"/detail/{}".format(news_id)}
                }
                return Response({"code":0,"errmsg":"ok","news":news_info})
            else:
                return Response({"code":400,"errmsg":"newsDoNotExist"})
        except Exception as e:
            print(e)
            return Response({"code":400,"errmsg":e})

