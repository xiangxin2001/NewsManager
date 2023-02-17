from django.urls import path,include
from apscheduler.scheduler import Scheduler 
from .views import Sprider_data_in
sched = Scheduler()  #实例化，固定格式
 
@sched.interval_schedule(seconds=1800)  #装饰器，seconds=60意思为该函数为1分钟运行一次
def mytask():  
    Sprider_data_in()  
  
sched.start()  #启动该脚本

urlpatterns = [

]