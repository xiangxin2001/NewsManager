import requests
import json
import time
from pathlib import Path
import random
BASE_DIR = Path(__file__).resolve().parent


#定义爬虫类
class Web_Sprider:
    def __init__(self,url:str,name:str,example:str,categroy:str,categroy_num_list:list) -> None:
        self.url,self.name,self.example,self.categroy_num_list = url,name,example,categroy_num_list
        #设置请求头
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.78"
        }
        self.categroy_list=categroy.split(",")
        self.dataset={}

    def main(self) -> None:
        self.get_news_list()
        #获取解析规则
        with open(BASE_DIR/"parse_rule.json","r",encoding="utf-8") as f:
            parse_rule_dict=json.load(f)
            re_rule=parse_rule_dict[self.name]["re"]
            xpath=parse_rule_dict[self.name]["xpath"]
            # print(parse_rule_dict[self.name]["re"])
        if self.parse_news_list(rule=re_rule):
            self.get_news_detail()
            self.save()
        self.parse_news_detail(xpath=xpath)
        
    #解析网页获取新闻列表    
    def parse_news_list(self,rule:str)->bool:
        self.news_list_dict={}
        # dataset={}
        # with open(BASE_DIR/"test.json","r",encoding="utf-8") as f:
        #     dataset=json.load(f)
        for keyword in self.categroy_list:
            parser=Html_parser_re(data=self.dataset[keyword],rule=rule)
            news_list=parser.main()
            if news_list:
                self.news_list_dict[keyword]=news_list
            else:
                return False
        # print(self.news_list_dict)
        return True
    #爬取新闻列表数据
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
    #解析网页获取新闻
    def parse_news_detail(self,xpath:str)->bool:
        news={"title":[],"category":[],"passage":[],"news_from":[],"url":[]}
        # news_detail_dict={}
        # with open(BASE_DIR/"data.json","r",encoding="utf-8") as f:
        #     dict=json.load(f)
        #     news_detail_dict=dict["news_detail_dict"]
        for keyword in self.categroy_list:
            for news_detail in self.news_detail_dict[keyword]:
                parser=Html_parser_xpath(data=news_detail['data'],xpath=xpath)
                passage=parser.main()
                if passage is not None:
                    news["title"].append(news_detail["title"])
                    news["category"].append(self.categroy_num_list[self.categroy_list.index(keyword)])
                    news["passage"].append(passage)
                    news["news_from"].append(self.name)
                    news["url"].append(news_detail["url"])
                    print("解析成功！")
                else:
                    print("出错！请检查解析规则或数据")
        import pandas
        news_csv=pandas.DataFrame(news,columns=["title","category","passage","url"])
        news_csv.to_csv(BASE_DIR/"news.csv",index=True,encoding='utf-8')
        return True

    #爬取新闻详情页
    def get_news_detail(self)->None:
        self.news_detail_dict={}
        for keyword in self.categroy_list:
            news_detail_list=[]
            for item in self.news_list_dict[keyword]:
                url=item['url']
                title=item['title']
                print("-----正在爬取网页{}-----".format(url))
                data:str
                if self.name=="人民网":
                    data=requests.get(url="http://{a}.people.com.cn{b}".format(a=keyword,b=url),headers=self.headers).content.decode("utf-8")
                else:
                    data=requests.get(url="http://{}".format(url),headers=self.headers).content.decode("utf-8")
                if data:
                    print("-----网页{}爬取成功-----".format(url))
                    news_detail_list.append({"url":url,"title":title,"data":data})
                    #实验性删除
                    del item
                    time.sleep(random.uniform(0.5,1.2))
                else:
                    print("-----网页爬取失败-----")
            self.news_detail_dict[keyword]=news_detail_list


    def save(self) -> bool:
        with open(BASE_DIR/"data.json","w",encoding="utf-8") as f:
            ds={}
            ds["news_list_dict"]=self.news_list_dict
            ds["dataset"]=self.dataset
            ds["news_detail_dict"]=self.news_detail_dict
            json.dump(ds,f,ensure_ascii=False)
        return True


#使用正则解析网页
class Html_parser_re:
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
                news_list.append({"url":news[0],"title":news[1]})
            print("网页解析成功")
        else:
            print("result_list列表为空，请检查解析规则或数据")
        return news_list

#使用XPath解析网页
class Html_parser_xpath:
    def __init__(self,data:str,xpath:str) -> None:
        self.data,self.xpath=data,xpath

    def main(self) -> str:
        return self.parsing()

    def parsing(self) -> str:
        from lxml import etree
        from xml.etree.ElementTree import tostring
        html=etree.HTML(self.data)
        passage:str
        passage_xpath=html.xpath(self.xpath)
        if passage_xpath:
            for passage_piece in passage_xpath:
                passage += tostring(passage_piece,encoding="utf-8").decode("utf-8")
        return passage

class main:
    #主程序
    def main(self):
    #从本地获取目标列表
        target_list={}
        with open(BASE_DIR/"target.json","r",encoding="utf-8") as f:
            target_list=json.load(f)
            target_list=target_list["test"]
        if target_list:
            for target in target_list:
                web_sprider=Web_Sprider(url=target["url"],name=target["name"],example=target["example"],categroy=target["categroy"],categroy_num_list=target["categroy_num_list"])
                web_sprider.main()

# test=main()
# test.main()
