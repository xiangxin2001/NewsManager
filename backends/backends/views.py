from django.middleware.csrf import get_token
from rest_framework.views import APIView
from rest_framework.response import Response
class get_tokenAPI(APIView):
    def get(self,request):
        csrf_token = get_token(request)  # 获取csrf_token的值

        return Response({'csrf_token': csrf_token})
