from django.shortcuts import render
from utils.sprider.sprider import main,BASE_DIR
from .models import News,Category
import pandas
# Create your views here.
#爬取的新闻入库
def Sprider_data_in():
    main.main()
    data_dict=pandas.read_csv(BASE_DIR/'news.csv',index_col=0, squeeze=True).to_dict()
    for i in data_dict['title'].keys():
        if not News.objects.filter(title=data_dict['title'][i]):
            News.objects.create(title=data_dict['title'][i],category=Category.objects.get(id=data_dict['category'][i]+1),passage=data_dict['passage'][i],url=data_dict['url'][i])
            print("新闻{}入库".format(data_dict['title'][i]))
        else:
            print("数据重复")
    
# Category.objects.create(name="财经")
# Category.objects.create(name="娱乐")