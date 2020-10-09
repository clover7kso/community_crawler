import re
import csv
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Manager
from datetime import date
from datetime import datetime
from datetime import time
import time as t
import random
# 시작 URL
BASE_URL = "https://www.fmkorea.com/index.php?mid=best&listStyle=list&page="


def timedelta2int(td):
    res = round(td.microseconds/float(1000000)) + \
        (td.seconds + td.days * 24 * 3600)
    return res


# ------------------------크롤링------------------------------
def getData():

    startPage = 0
    while True:

        startPage = startPage + 1

        t.sleep(random.randint(5, 10))
        reqUrl = Request(BASE_URL+str(startPage),
                         headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(reqUrl)
        soup = BeautifulSoup(html, "html.parser")

        soup = soup.find("tbody")
        lastTime = datetime.now()
        for i in soup.find_all('tr'):
            title = i.find("a", "hx").text.strip()
            replyNum = i.find("a", "replyNum").text.strip().replace(",", "")
            timeString = i.find("td", "time").text.strip().split(":")
            timeValue = datetime.combine(
                date.today(), time(int(timeString[0]), int(timeString[1])))
            if timedelta2int(lastTime-timeValue) < 0:
                return
            voteNum = i.find_all("td", "m_no")[0].text.strip().replace(",", "")
            viewNum = i.find_all("td", "m_no")[1].text.strip().replace(",", "")
            print("제목 : ", title, " 댓글수 : ", replyNum, " 시간 : ", timeValue.strftime("%Y/%m/%d, %H:%M:%S"),
                  " 추천수 : ", voteNum, " 조회수 : ", viewNum)


if __name__ == '__main__':
    getData()
