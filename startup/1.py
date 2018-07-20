# coding:utf-8

import urllib.request
from bs4 import BeautifulSoup

url = 'http://www.youyourentiyishu.com/rentiyishuxiezhen?pn='


def download(url):
    html = urllib.request.urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    #img_list = bs.find_all('img', class_="imageitem")
    img_list = bs.select('.imageitem a')

    for i in img_list:
        imgurl = i.get('src')
        yield imgurl


def get_all_image(n):
    imgurls = []
    for k in range(1, n):
        ur = url + str(k)
        try:
            imgurls.extend(list(download(ur)))
        except Exception as e:
            pass
    return imgurls

def save_img_to_file(n):
    imgurls = get_all_image(n)
    for i, imgurl in enumerate(imgurls):
        try:
            urllib.request.urlretrieve(imgurl, 'img/%s.jpg' % i)
            print('Downloading %s picture now!!!' % i)
        except Exception as e:
            pass


