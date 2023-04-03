from django.urls import path
from . import views
from apscheduler.scheduler import Scheduler
sched = Scheduler()  #实例化，固定格式 
@sched.interval_schedule(seconds=86400)  #装饰器，seconds=60意思为该函数为1分钟运行一次
def con_usercharacters():  
    views.calculate_usercharacters()
  
sched.start()  #启动该脚本


urlpatterns = [
    path('username/<str:username>/count/',views.usernameCountAPI.as_view()),
    path('register/new/',views.registerNewAPI.as_view()),
    path('email/<str:email>/count/',views.emailCountAPI.as_view()),
    path('mobile/<str:mobile>/count/',views.mobileCountAPI.as_view()),
    path('login/userlogin/',views.userloginAPI.as_view()),
    path('logout/',views.logoutAPI.as_view()),
    path('info/',views.centerViewAPI.as_view()),
    path('password/',views.passwordChangeAPI.as_view()),
]
