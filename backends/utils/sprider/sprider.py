from news.models import News
import requests
import json
#从本地获取目标列表
target_list={}
with open("target.json","r",encoding="utf-8") as f:
    target_list=json.load(f)
    target_list=target_list["target_list"]
3