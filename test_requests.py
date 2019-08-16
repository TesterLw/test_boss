import requests
from lxml import etree
import time

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36"
}

def send_url():
    parm = {"query": "测试",
            "city": "101280100"
            }
    url = "https://www.zhipin.com/job_detail/"
    r = requests.get(url,params=parm,headers=headers)
    html = r.content.decode('utf-8')
    print(html)
    return html

def job_urls():
    html = send_url()

    html_obj = etree.HTML(html)
    nodes = html_obj.xpath(".//div[@class='info-primary']//a/@href")
    job_url = []
    for node in nodes:
        detail_url = '/'.join(["https://www.zhipin.com", node])
        job_url.append(detail_url)
    return job_url



def xml():
    job_url = job_urls()
    items={}
    for i in  job_url:
        html = requests.get(url=i,headers=headers)
        html = html.text.replace('<br/>','').replace('\n','').encode('utf-8')
        html = etree.HTML(html)
        Company     = html.xpath("//*[@class='sider-company']/div/a[2]/text()")[0].replace(' ','')
        description = html.xpath("//*[@id='main']/div[3]/div/div[2]/div[2]/div[1]/div/text()")[0].replace(' ','')
        Recruiters  = html.xpath("//*[@id='main']/div[3]/div/div[2]/div[1]/h2/text()").replace('','')
        items.setdefault(Company,{})['招聘人'] = Recruiters
        items.setdefault(Company,{})['学历要求']=html.xpath("//*[@id='main']/div[1]/div/div/div[2]/p/text()")[2]
        items.setdefault(Company,{})['经验要求']=html.xpath("//*[@id='main']/div[1]/div/div/div[2]/p/text()")[1]
        items.setdefault(Company,{})['薪资'] = html.xpath("//*[@id='main']/div[1]/div/div/div[2]/div[2]/span/text()")[0]
        items.setdefault(Company,{})['职位具体要求']=description
        time.sleep(20)
    return items

