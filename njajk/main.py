import logging
import  urllib.request
import  time
import  datetime
import pymysql
from collections import deque
from bs4 import BeautifulSoup
def configLog():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a, %d %b %Y %H:%M:%S',
                        filename='log/info.log',
                        filemode='a')

def retrivie_links():
    cur = db_conn.cursor();
    sql_text = "select * from house365"
    row_num = cur.execute(sql_text)
    all_url = cur.fetchall()
    url_list = deque()
    for (a,b) in all_url:
        url_list.append(a)
    return  url_list

def main():
    logging.info("This is function of main!")
    #IterateInfoList(entry_url)
    ParseAndSaveHouseDetail()
    #ParseHouseDetail("http://nj.sell.house365.com/s_133257756.html")




################################################################################
entry_url = "http://nj.sell.house365.com/district/"
house_queue = deque()
db_conn = pymysql.connect(host="127.0.0.1",port=3306,user="root",password="root123",db='spiderdata')
################################################################################
def ParseAndSaveHouseDetail():
    my_queue=retrivie_links()
    while my_queue:
        url =  my_queue.popleft()
        ParseHouseDetail(url)
        time.sleep(1)

def ParseHouseDetail(url):
    response = urllib.request.urlopen(url)
    bs = BeautifulSoup(response, 'html.parser',from_encoding="gb18030")
    #detail_info_list_field=bs.select("div.person_info .gr_table dt")
    #detail_info_list_vlaue = bs.select("div.person_info .gr_table dd")
    detail_list = bs.select("div.person_info .gr_table dl")
    for item in detail_list:
        try:
            item_name = item.find("dt").get_text()
            #print(item_name)
            if item_name=="售价：":
                item_value = item.find("i").get_text()
            elif item_name=="小区：":
                item_value = item.find("a").get_text()
            else:
                item_value = item.find("dd").get_text()

            logging.info(item_name + item_value)
            print(item_name, item_value)



        except Exception as e:
            logging.info(url,e)





def parseAllInfoList(url):
    try:
        response = urllib.request.urlopen(url)
        bs = BeautifulSoup(response, 'html.parser')
        info_list = bs.select("div .info_list")
        cur = db_conn.cursor();
        for item in info_list:
            url = item.get("data-url")
            house_queue.append(url)
            #sqlText = "insert into house365(url,crawl_time) values('{0}',now())".format(url)
            #logging.info(sqlText)
            #cur.execute(sqlText)

        db_conn.commit()
        cur.close()
    except Exception as e:
        print(e)
        pass


def IterateInfoList(url):
     page_no = range(1,100)
     for i in page_no:
         page_url = "{0}dl_p{1}.html"
         page_url = page_url.format(url,i)
         parseAllInfoList(page_url)




if __name__ == '__main__':
    configLog()
    logging.info("这是一个伟大的开端")
    logging.info("let's roll!")
    main()
    logging.info("here we are!")

