from bs4 import BeautifulSoup
from urllib.request import urlopen, urljoin, Request
import re
import base64
import subprocess
import sys

node_url_1 = "https://view.freev2ray.org/"
node_url_2 = "https://jichangdaquan.com/node/429.html"
file_abs_name = 'v.md'

def crawl(web_url):
    headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:52.0) Gecko/20100101 Firefox/52.0",
            "Accept": "*/*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Accept-Encoding": "",
            "Connection": "keep-alive",
            }
    req = Request(url=web_url, headers=headers)
    response = urlopen(req)
    return response.read().decode()


def parse_1(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find('button', {"class": "copybtn"}).attrs 
    return urls['data-clipboard-text']


def parse_2(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find_all('a', {"id": re.compile('v2ray.')}) 
    urls_code = []
    for url in urls:
        urls_code.append(url.attrs['href'])
    return urls_code


# base64编码
def base64encode(text):
    return str(base64.b64encode(text.encode('utf-8')),'utf-8')


# base64解码
def base64decode(code):
    return base64.b64decode(code)


# 写文件
def write_md(b64_text,file):
    with open(file,'w') as f:
        f.write(b64_text)


# 更新订阅器
def update_git():
    status = subprocess.run(["git", "status"])
    print(status)

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m","update node"])
    subprocess.run(["git", "push", "origin", "master"])
 
if __name__ == '__main__':
    # 获取节点
    url = []
    html = crawl(node_url_1)
    url_1 = parse_1(html)
    for node in url_1:
        url.append(node)

    html = crawl(node_url_2)
    url_2 = parse_2(html)
    for node in url_2:
        url.append(node)

    if url:
        b64_url = url[0]
        url = url[1:]
        for node in url:
            b64_url = b64_url + '\n' + node
        b64_url = base64encode(b64_url)
    else:
        print("can not get url")

    # 写入文件
    write_md(b64_url,file_abs_name)

    # 更新订阅器 
    update_git()

    print("success")