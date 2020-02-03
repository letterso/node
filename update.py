from bs4 import BeautifulSoup
from urllib.request import urlopen, urljoin
import re
import base64
import subprocess
import sys

node_url_1 = "https://view.freev2ray.org/"
file_abs_name = 'E:/documen/github/node/v.md'

def crawl(url):
    response = urlopen(url)
    return response.read().decode()


def parse_1(html):
    soup = BeautifulSoup(html, 'lxml')
    urls = soup.find('button', {"class": "copybtn"}).attrs 
    return urls['data-clipboard-text']


# 返回base64编码
def base64encode(text):
    return str(base64.b64encode(text.encode('utf-8')),'utf-8')


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
    html = crawl(node_url_1)
    url_1 = parse_1(html)
    if url_1:
        b64_url = base64encode(url_1)
        print(url_1)
    else:
        print("can not get url")

    # 写入文件
    write_md(b64_url,file_abs_name)

    # 更新订阅器 
    update_git()

    print("success")