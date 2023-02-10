# from news.models import News
import requests
import json
import time
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent
#定义爬虫类
class Web_Sprider:
    def __init__(self,url:str,name:str,example:str,categroy:str) -> None:
        self.url,self.name,self.example,self.categroy = url,name,example,categroy
        #设置请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
        }
        self.categroy_list=self.categroy.split(",")
        self.dataset={}

    def main(self) -> None:
        self.get_news_list()
        #获取解析规则
        with open(BASE_DIR/"parse_rule.json","r",encoding="utf-8") as f:
            parse_rule_dict=json.load(f)
            # print(parse_rule_dict[self.name])
            self.parse_news_list(parse_rule_dict[self.name])
        self.save()
        
    def parse_news_list(self,rule:str)->bool:
        self.news_dict={}
        dataset={}
        with open(BASE_DIR/"test.json","r",encoding="utf-8") as f:
            dataset=json.load(f)
        for keyword in self.categroy_list:
            parser=Html_parser_re(data=dataset[keyword],rule=rule)
            news_list=parser.main()
            if news_list:
                self.news_dict[keyword]=news_list
            else:
                return False
        # print(self.news_dict)
        return True

    def get_news_list(self) -> None:
        
        #组装url并爬取网页,获取新闻列表
        for keyword in self.categroy_list:
            print("-----正在爬取网页{}-----".format(self.example.format(keyword)))
            data=requests.get(url=self.example.format(keyword),headers=self.headers).content.decode("utf-8")
            if data:
                print("-----网页{}爬取成功-----".format(self.example.format(keyword)))
                self.dataset[keyword]=data
                time.sleep(2)
            else:
                print("-----网页爬取失败-----")
                break
    
    def save(self) -> bool:
        with open(BASE_DIR/"data.json","w",encoding="utf-8") as f:
            ds={}
            ds["news_dict"]=self.news_dict
            ds["dataset"]=self.dataset
            json.dump(ds,f,ensure_ascii=False)
        return True
#网页解析
class Html_parser_re():
    def __init__(self,data:str,rule:str) -> None:
        self.data,self.rule=data,rule

    def main(self)->list:
        return self.parsing()

    def parsing(self)->list:
        import re
        r= re.compile(self.rule)
        result_list=r.findall(self.data)
        news_list=[]
        if result_list:
            for news in result_list:
                news_list.append({"url":news[0],"name":news[1]})
            print("网页解析成功")
        else:
            print("result_list列表为空，请检查解析规则或数据")
        return news_list



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