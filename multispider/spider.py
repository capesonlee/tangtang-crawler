import urllib.request
import time
import  threading
from bs4 import BeautifulSoup
from collections import deque


imge_queue = deque()
class ImgDownloader(threading.Thread):

    def __init__(self,threadId,name,q):
        threading.Thread.__init__(self)
        self.threadId= threadId;
        self.name = name
        self.q =q
        #print("init thread %s name:%s" %(threadId,name) )
    def run(self):
        wait_secs = 0.5
        while wait_secs < 128:
            #print(self.name, self.threadId, wait_secs,len(self.q))
            try:
                if not self.q:
                    time.sleep(wait_secs)
                    wait_secs*=2
                    continue
                else:
                    wait_secs = 0.5
                img_url = self.q.popleft()
                self.save_img_to_file(img_url)
                time.sleep(0.2)
            except Exception as e:
                print(e)
                pass
        print(self.name, self.threadId, "stopped")

    def save_img_to_file(self,img_url):
        try:
            suffix = get_url_palin_suffix(img_url)
            if is_type_of_img(suffix) != True:
                pass
                #print("not image file format", img_url)
                return
            filename = get_file_name_from_url(img_url)
            if '-200x0' in filename or "-0x200" in filename or '-400x0' in filename or "-0x400" in filename:
                pass
                return

            urllib.request.urlretrieve(img_url, 'img/%s' % filename)
            #print('Downloading %s picture now!!!' % filename)
        except Exception as e:
            print(e,img_url)
            pass

class HtmlProcessor(threading.Thread):

    url_set = {'javascript:scroll(0,0)', '#', ''}
    url_set_lock = threading.Lock()
    urlQueue = deque()

    def __init__(self,threadId,name,imgQueue):
        threading.Thread.__init__(self)
        self.threadId = threadId
        self.name = name
        self.imgQueue = imgQueue

        print("init thread %s name:%s" % (threadId, name))


    def run(self):
        wait_secs = 0.5
        while wait_secs < 128:
            time.sleep(0.5)
            #print(self.name,self.threadId,wait_secs)
            if not self.urlQueue:
                time.sleep(wait_secs)
                wait_secs *= 2
                continue
            else:
                wait_secs = 0.5
            url_item = self.urlQueue.popleft()
            suffix = get_url_palin_suffix(url_item)
            if is_type_of_html(suffix):
                self.process_html_file(url_item)

            else:
                pass
                #print("not supported url:", url_item)
        print(self.name,self.threadId,"stopped")

    def process_html_file(self,url):
        try:
            #print("processing url: ", url)
            html = urllib.request.urlopen(url,timeout=5)
            bs = BeautifulSoup(html, 'html.parser')
            html_item_list = bs.find_all("a")

            for item in html_item_list:
                url = item.get("href")
                if url.find("http") == 0 and "youyourentiyishu" not in url:
                    #print("other websit: ", url)
                    continue

                url = convert_relative_url(url)
                if url not in self.url_set:
                    self.urlQueue.append(url)
                    #print("size of url queue",self.threadId, len(self.urlQueue))
                    self.url_set_lock.acquire()
                    self.url_set.add(url)
                    self.url_set_lock.release()
                else:
                    pass

            img_item_list = bs.find_all("img")
            for item in img_item_list:
                url = item.get("src")
                url = convert_relative_url(url)

                if url not in self.url_set :
                   self.imgQueue.append(url)

                   self.url_set_lock.acquire()
                   self.url_set.add(url)
                   self.url_set_lock.release()
                else:
                    pass

        except Exception as e:
            print("ThreadId",self.threadId,e,url)
            pass


init_url = 'http://www.youyourentiyishu.com/'


def convert_relative_url(url):

    if url.find('http') != 0 :
        return  init_url + url
    return url





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

class ThreadMonitor(threading.Thread):
    def __init__(self,imgThreads,htmlThreads):
        threading.Thread.__init__(self)
        self.imgThreads = imgThreads
        self.htmlThreads = htmlThreads

    def run(self):
        while True:
            print("#######################################################################")
            for t in self.imgThreads:
                print(t.name,t.threadId,t.is_alive(),len(t.q))

            print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")

            for t in self.htmlThreads:
                print(t.name,t.threadId,t.is_alive(),len(t.urlQueue))
            time.sleep(16)

def main():
    HtmlProcessor.urlQueue.append(init_url)

    img_threads = []
    for i in range(5):
        t = ImgDownloader(i,"dld_img",imge_queue)
        t.setDaemon(True)
        t.start()
        img_threads.append(t)

    html_threads = []
    for i in range(10):
        t = HtmlProcessor(i,"pcs_html",imge_queue)
        t.setDaemon(True)
        t.start()
        html_threads.append(t)

    t = ThreadMonitor(img_threads,html_threads)
    t.setDaemon(True)
    t.start()

    print("here are image threads")
    for t in img_threads:
        t.join()

    print("here are html threads")
    for t in html_threads:
        t.join()


    print("it is done")

if __name__ == '__main__':
    main()




