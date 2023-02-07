# from news.models import News
import requests
import json
import time
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
#定义爬虫类
class Web_Sprider:
    def __init__(self,url,name,example,categroy):
        self.url,self.name,self.example,self.categroy = url,name,example,categroy
        #设置请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
        }

    def main(self):
        self.get_data()
        self.save()

    def get_data(self):
        categroy_list=self.categroy.split(",")
        self.dataset={}
        #组装url并爬取网页
        for keyword in categroy_list:
            print("-----正在爬取网页{}-----".format(self.example.format(keyword)))
            data=requests.get(url=self.example.format(keyword),headers=self.headers).content.decode("utf-8")
            if data:
                print("-----网页{}爬取成功-----".format(self.example.format(keyword)))
                self.dataset[keyword]=data
                time.sleep(2)
            else:
                print("-----网页爬取失败-----")
                break
    
    def save(self):
        with open(BASE_DIR/"data.json","w",encoding="utf-8") as f:
            json.dump(self.dataset,f,ensure_ascii=False)


        

if __name__=="__main__":
    #从本地获取目标列表
    target_list={}
    with open(BASE_DIR/"target.json","r",encoding="utf-8") as f:
        target_list=json.load(f)
        target_list=target_list["test"]
    if target_list:
        for target in target_list:
            web_sprider=Web_Sprider(url=target["url"],name=target["name"],example=target["example"],categroy=target["categroy"])
            web_sprider.main()