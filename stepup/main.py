import urllib.request
import time
from bs4 import BeautifulSoup
from collections import deque

init_url = 'http://www.youyourentiyishu.com/'
queue = deque()
visited = {'javascript:scroll(0,0)','#',''}


def start_crawl(url):
    global visited
    queue.append(url)

    while queue:
        url = queue.popleft()
        visited |= {url }
        print("visited links: ", len(visited),"queue size:",len(queue))

        suffix = get_url_palin_suffix(url)
        if is_type_of_img(suffix):
            save_img_to_file(url)
        elif is_type_of_html(suffix):
            process_html_file(url)
        else:
            print("not supportted url: ", url)

        time.sleep(0.3)

def convert_relative_url(url):
    if url in visited:
        return  url

    if url.find('http') != 0 :
        return  init_url + url
    return url

def process_html_file(url):
    try:
        print("processing url: ", url)
        html = urllib.request.urlopen(url)
        bs = BeautifulSoup(html, 'html.parser')
        html_item_list = bs.find_all("a")
        for item in html_item_list:
            url = item.get("href")
            if url.find("http")==0 and "youyourentiyishu" not in url:
                print("other websit: ",url)
                continue

            url = convert_relative_url(url)

            if url not in visited and url not in queue:
                queue.append(url)
            else:
                pass

        img_item_list = bs.find_all("img")
        for item in img_item_list:
            url = item.get("src")
            url = convert_relative_url(url)
            if url not in visited:
                queue.append(url)
            else:
                pass
    except Exception as e:
        print(e)
        pass


def save_img_to_file(img_url):
    try:

        filename = get_file_name_from_url(img_url)
        if '-200x0' in filename or "-0x200" in filename:
            print("we do not process thumbfile",img_url)
            return

        urllib.request.urlretrieve(img_url, 'img/%s' % filename)
        print('Downloading %s picture now!!!' % filename)
    except Exception as e:
        print(e)
        pass


def get_file_name_from_url(url):
    parsed_url = urllib.request.urlparse(url)
    all_path = parsed_url.path.split("/")
    file_name = all_path[len(all_path) - 1]
    return file_name


def get_url_palin_suffix(url):
    filename = get_file_name_from_url(url)
    if "." not in filename:
        return "html"  # 暂时按html处理

    file_name_suffix = filename.split(".")
    suffix = filename.split(".")[len(file_name_suffix) - 1]
    return suffix


def is_type_of_img(suffix):
    return suffix == "jpg"


def is_type_of_html(suffix):
    return suffix == "html" or suffix == "htm"


if __name__ == '__main__':
    start_crawl(init_url)
