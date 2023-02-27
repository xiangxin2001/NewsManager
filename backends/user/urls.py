from django.urls import path
from . import views

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
