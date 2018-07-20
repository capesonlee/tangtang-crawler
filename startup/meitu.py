
# coding:utf-8
import  re
import urllib.request
from bs4 import BeautifulSoup

url = 'http://www.youyourentiyishu.com/rentiyishuxiezhen'

def get_beautiy_url(url):
    html = urllib.request.urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    beautiy_list = bs.select('.imageitem a')
    for a in beautiy_list:
        beautiy_url = a.get("href")
        yield  beautiy_url

def get_beautiy_url_list(url):
    url_list = []
    try:
        url_list.extend(list(get_beautiy_url(url)))
    except Exception as e:
        pass
    return url_list

def process_beauty_url_list(url_list):
    for beauty_url in url_list:
        save_img_to_file(beauty_url)


def save_img_to_file(img_url):
    try:
        filename=re.findall(r'(?<=/).+?(?=.)',img_url)
        print(filename)
        # urllib.request.urlretrieve(img_url, 'img/%s.jpg' % i)
        print('Downloading %s picture now!!!' % filename)
    except Exception as e:
        print(e)
        pass

def download_all(url):
    url_list = get_beautiy_url_list(url)
    process_beauty_url_list(url_list)

if __name__ == '__main__':
    download_all(url)