from django.urls import path
from apscheduler.scheduler import Scheduler 
from .views import Sprider_data_in
sched = Scheduler()  #实例化，固定格式
from .views import News_detailAPI,News_categoryAPI,NewsSearchView
@sched.interval_schedule(seconds=1800)  #装饰器，seconds=60意思为该函数为1分钟运行一次
def mytask():  
    Sprider_data_in()  
  
sched.start()  #启动该脚本

urlpatterns = [
    path('news/<str:news_id>',News_detailAPI.as_view()),
    path('news/category/<str:category_id>',News_categoryAPI.as_view()),
    path('search',NewsSearchView()),
]