import re
import csv
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Manager
from datetime import date
from datetime import datetime
from datetime import time
import pymysql
# 시작 URL
BASE_URL = "https://gall.dcinside.com/board/lists/?id=baseball_new9&list_num=100&sort_type=N&exception_mode=recommend&search_head=&page="

conn = pymysql.connect(host='crawler-database.c4bvdospxfm8.ap-northeast-2.rds.amazonaws.com',
                       user='killca', password='!comkbg702bk', db='crawler_data', charset='utf8')
cursor = conn.cursor()
sql = "INSERT INTO crawler_table (url, title, replyNum, viewNum, voteNum, timeUpload) VALUES (%s, %s, %s, %s, %s, %s) ON DUPLICATE KEY UPDATE"

# ------------------------크롤링------------------------------


def getData():

    startPage = 0

    while True:

        startPage = startPage + 1

        reqUrl = Request(BASE_URL+str(startPage),
                         headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(reqUrl)
        soup = BeautifulSoup(html, "html.parser")

        soup = soup.find("tbody")
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        for i in soup.find_all('tr'):
            if i.find("td", "gall_num").text.strip() == "설문" or i.find("td", "gall_num").text.strip() == "공지":
                continue
            url = "https://gall.dcinside.com" + \
                i.find("td", "gall_tit ub-word").find_all("a")[0]['href']
            title = i.find(
                "td", "gall_tit ub-word").find_all("a")[0].text.strip()
            replyNum = i.find(
                "td", "gall_tit ub-word").find_all("a")[1].text.strip().replace(
                "[", "").replace("]", "").replace(",", "")
            timeString = i.find("td", "gall_date")['title']
            timeValue = datetime.strptime(
                timeString, '%Y-%m-%d %H:%M:%S')

            if((today-timeValue.replace(hour=0, minute=0, second=0, microsecond=0)).days >= 1):
                conn.commit()
                conn.close()
                return

            voteNum = i.find(
                "td", "gall_recommend").text.strip().replace(",", "")
            viewNum = i.find("td", "gall_count").text.strip().replace(",", "")

            cursor.execute(sql, (url, title, replyNum, viewNum,
                                 voteNum, timeValue.strftime("%Y-%m-%d %H:%M:%S")))
            print("URL : ", url, "제목 : ", title, " 댓글수 : ", replyNum, " 시간 : ", timeValue.strftime("%Y-%m-%d %H:%M:%S"),
                  " 추천수 : ", voteNum, " 조회수 : ", viewNum)


if __name__ == '__main__':
    getData()
