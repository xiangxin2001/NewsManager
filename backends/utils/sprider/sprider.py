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
        with open(BASE_DIR/'dataset.json','w',encoding='utf-8') as f:
            json.dump(self.dataset,f,ensure_ascii=False)
        #获取解析规则
        with open(BASE_DIR/"parse_rule.json","r",encoding="utf-8") as f:
            parse_rule_dict=json.load(f)
            re_rule_dict=parse_rule_dict[self.name]["re"]
            xpath_dict=parse_rule_dict[self.name]["xpath"]
            
        self.parse_news_list(rule_dict=re_rule_dict)
        if self.news_list_dict is not None:
            self.get_news_detail()
            
            if self.news_detail_dict is not None:
                self.save()
                self.parse_news_detail(xpath_dict=xpath_dict)
            else:
                print("news_detail_dict为空，请检查")
        else:
            print("news_list_dict为空，请检查")
        
    #解析网页获取新闻列表    
    def parse_news_list(self,rule_dict:dict)->None:
        self.news_list_dict={}
        # dataset={}
        # with open(BASE_DIR/"{}_data.json".format(self.name),"r",encoding="utf-8") as f:
        #     dataset=json.load(f)
        #     # dataset=dataset["dataset"]
        for keyword in self.categroy_list:
            rule_list=rule_dict[keyword]
            parser=Html_parser_re(data=self.dataset[keyword],rule_list=rule_list)
            news_list=parser.main()
            self.news_list_dict[keyword]=news_list
            
        # print(self.news_list_dict)
        
    #爬取新闻列表数据
    def get_news_list(self) -> None:
        
        #组装url并爬取网页,获取新闻列表
        for keyword in self.categroy_list:
            flag=True
            try:
                print("-----正在爬取网页{}-----".format(self.example.format(keyword)))
                data=requests.get(url=self.example.format(keyword),headers=self.headers,timeout=20).content
            except Exception as e:
                print(str(e))
                flag=False
            if flag:
                try:
                    data=data.decode('utf-8')
                except Exception as e:
                    print(str(e))
                    data=data.decode('gbk')
                    
                # print(data)
                if data:
                    print("-----网页{}爬取成功-----".format(self.example.format(keyword)))
                    self.dataset[keyword]=data
                    # time.sleep(random.uniform(1.2,2.0))
            else:
                self.dataset[keyword]=""
                print("-----网页爬取失败-----")
                
    #解析网页获取新闻
    def parse_news_detail(self,xpath_dict:dict)->bool:
        news={"title":[],"category":[],"passage":[],"news_from":[],"url":[]}
        # news_detail_dict={}
        # with open(BASE_DIR/"{}_data.json".format(self.name),"r",encoding="utf-8") as f:
        #     dict=json.load(f)
        #     news_detail_dict=dict["news_detail_dict"]
        for keyword in self.categroy_list:
            for news_detail in self.news_detail_dict[keyword]:
                xpath=xpath_dict[keyword]
                parser=Html_parser_xpath(data=news_detail['data'],xpath=xpath)
                passage=parser.main()
                if passage is not None and len(passage)>20:
                    news["title"].append(news_detail["title"])
                    news["category"].append(self.categroy_num_list[self.categroy_list.index(keyword)])
                    news["passage"].append(passage)
                    news["news_from"].append(self.name)
                    news["url"].append(news_detail["url"])
                    print("解析成功！")
                else:
                    print("出错！请检查解析规则或数据")
        import pandas
        news_csv=pandas.DataFrame(news,columns=["title","category","passage","news_from","url"])
        news_csv.to_csv(BASE_DIR/"{}.csv".format(self.name),index=True,encoding='utf-8')
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
                flag=True
                data:object
                import re
                try:
                    if re.match(r"http.*://.*?",url) is not None:
                        print("原生")
                        data=requests.get(url=url,headers=self.headers,timeout=20).content
                    else:
                        if self.name=="人民网":
                            url="http://{}.people.com.cn{}".format(keyword,url)
                            print("人民网{}".format(url))
                            
                            data=requests.get(url=url,headers=self.headers,timeout=20).content
                        elif url[0]=='/':
                            url="{}{}".format(self.url,url)
                            print("后{}".format(url))
                            
                            data=requests.get(url=url,headers=self.headers,timeout=20).content
                        else:
                            url="http://{}".format(url)
                            print("其他{}".format(url))
                            data=requests.get(url=url,headers=self.headers,timeout=20).content
                    
                except Exception as e:
                    print(str(e))
                    flag=False
                if flag:
                    try:
                        data=data.decode('utf-8')
                    except Exception as e:
                        print(str(e))
                        data=data.decode('gbk')
                    if data:
                        print("-----网页{}爬取成功-----".format(url))
                        news_detail_list.append({"url":url,"title":title,"data":data})
                        #实验性删除
                        del item
                        # time.sleep(random.uniform(1.5,3.0))
                else:
                        print("-----网页爬取失败-----")
            self.news_detail_dict[keyword]=news_detail_list


    def save(self) -> bool:
        with open(BASE_DIR/"{}_data.json".format(self.name),"w",encoding="utf-8") as f:
            ds={}
            ds["news_list_dict"]=self.news_list_dict
            ds["dataset"]=self.dataset
            ds["news_detail_dict"]=self.news_detail_dict
            json.dump(ds,f,ensure_ascii=False)
        return True


#使用正则解析网页
class Html_parser_re:
    def __init__(self,data:str,rule_list:list) -> None:
        self.data,self.rule_list=data,rule_list

    def main(self)->list:
        return self.parsing()

    def parsing(self)->list:
        import re
        news_list=[]
        for rule in self.rule_list:
            
            r= re.compile(rule)
            result_list=r.findall(self.data,re.S)
            
            if result_list:
                for news in result_list:
                    news_list.append({"url":news[0],"title":news[1]})
                print("网页解析成功")
                
                rule=rule.replace('(.*?)','.*?')
                self.data=re.sub(rule,"",self.data,flags=re.S)
        
            else:
                print("正则匹配查找失败，请检查解析规则或数据\n{}\n{}".format(type(rule),rule))

        return news_list

#使用XPath解析网页
class Html_parser_xpath:
    def __init__(self,data:str,xpath:str) -> None:
        self.data,self.xpath=data,xpath

    def main(self) -> str:
        self.data_clean()
        return self.parsing()

    #清除js里的注释
    def data_clean(self)->None:
        import re
        self.data = re.sub("<!--[\\s\\S]*?(?:-->)?","",self.data)
        self.data = re.sub("<!--[\\s\\S]*?-->?","",self.data)
        self.data = re.sub('<!---+>?','',self.data)
        self.data = re.sub("|<!(?![dD][oO][cC][tT][yY][pP][eE]|\\[CDATA\\[)[^>]*>?","",self.data)
        self.data = re.sub("|<[?][^>]*>?","",self.data)
        

    def parsing(self) -> str:
        from lxml import etree
        from xml.etree.ElementTree import tostring
        passage_r=""
        try:
            html=etree.HTML(self.data)
            
            passage_xpath=html.xpath(self.xpath)
            # print('Jieduan1')
            if passage_xpath:
                # print('Jieduan2')
                for passage_piece in passage_xpath:
                    passage_r += tostring(passage_piece,encoding="utf-8").decode("utf-8")
                # print('jieduan3\n{}\n{}'.format('--------------------------------',passage_r))
        except Exception as e:
            print(str(e))
   
        return passage_r

class main:
    #主程序
    def main(self):
    #从本地获取目标列表
        target_list={}
        with open(BASE_DIR/"target.json","r",encoding="utf-8") as f:
            target_list=json.load(f)
            target_list=target_list["target_list"]
        if target_list:
            for target in target_list:
                web_sprider=Web_Sprider(url=target["url"],name=target["name"],example=target["example"],categroy=target["categroy"],categroy_num_list=target["categroy_num_list"])
                web_sprider.main()

# test=main()
# test.main()
