# coding:utf-8

import urllib.request
import time
from bs4 import BeautifulSoup

url = 'http://www.youyourentiyishu.com/rentiyishuxiezhen'


def get_beautiy_url(url):
    print("start processing page url: %s" % url)
    time.sleep(0.5)
    html = urllib.request.urlopen(url)
    bs = BeautifulSoup(html, 'html.parser')
    beautiy_list = bs.select('.imageitem a')
    for a in beautiy_list:
        beautiy_url = a.get("href")
        yield beautiy_url


def get_beautiy_url_list(url):
    url_list = []
    try:
        url_list.extend(list(get_beautiy_url(url)))
    except Exception as e:
        pass
    return url_list


def process_beauty_url_list(url_list):
    for beauty_url in url_list:
        img_list = get_img_url_list(beauty_url)
        for img_url in img_list:
            save_img_to_file(img_url)
            time.sleep(0.5)


def get_img_url_list(beauty_url):
    img_list = []
    try:
        # img_list.extend(list(get_img_url(beauty_url)))
        head_img_url, next_beauty_url = get_img_url(beauty_url)
        img_list.append(head_img_url)
        file_name = get_file_name_from_url(beauty_url).split(".")[0]
        while next_beauty_url.find(file_name) > 0:
            img_url, next_beauty_url = get_img_url(next_beauty_url)
            img_list.append(img_url)
    except Exception as e:
        pass
    return img_list


def get_img_url(beauty_url):
    html = urllib.request.urlopen(beauty_url)
    bs = BeautifulSoup(html, 'html.parser')
    img_items = bs.select(".showimg a img")
    img_url = img_items[0].get("src")
    next_beauty_item = bs.select(".showimg a")
    next_beauty_url = next_beauty_item[0].get("href")

    return (img_url, next_beauty_url)


def get_file_name_from_url(img_url):
    parsed_url = urllib.request.urlparse(img_url)
    all_path = parsed_url.path.split("/")
    img_name = all_path[len(all_path) - 1]
    return img_name


def save_img_to_file(img_url):
    try:
        filename = get_file_name_from_url(img_url)

        urllib.request.urlretrieve(img_url, 'img/%s' % filename)
        print('Downloading %s picture now!!!' % filename)
    except Exception as e:
        print(e)
        pass


def download_all(url):
    for k in range(1, 8):
        page_url = url + "/%s" % k
        url_list = get_beautiy_url_list(page_url)
        time.sleep(1)
        process_beauty_url_list(url_list)
        time.sleep(1)


if __name__ == '__main__':
    download_all(url)
