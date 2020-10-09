import re
import csv
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Manager
from datetime import date
from datetime import datetime
from datetime import time
import requests
# 시작 URL
BASE_URL = "http://web.humoruniv.com/board/humor/list.html?table=pds&pg="


def timedelta2int(td):
    res = round(td.microseconds/float(1000000)) + \
        (td.seconds + td.days * 24 * 3600)
    return res


# ------------------------크롤링------------------------------
def getData():

    startPage = -1
    while True:

        startPage = startPage + 1
        headers = {
            'Referer': 'strict-origin-when-cross-origin',
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36"
        }
        reqUrl = requests.get(
            BASE_URL+str(startPage), headers=headers, verify=False)
        soup = BeautifulSoup(reqUrl.content.decode(
            'euc-kr', 'replace'), "html.parser")

        soup = soup.find("div", id="cnts_list_new").find_all("table")[1]
        lastTime = datetime.now()
        for i in soup.find_all('tr', id=re.compile('^li_chk_pds-')):
            replyNum = i.find("span", "list_comment_num").text.strip().replace(
                "[", "").replace("]", "").replace(",", "")
            title = i.find_all("a")[1]
            for tag in title.find_all("span"):
                tag.replaceWith('')
            title = title.get_text().strip()
            timeString = i.find("span", "w_time").text.strip().split(":")
            timeValue = datetime.combine(
                date.today(), time(int(timeString[0]), int(timeString[1])))
            if timedelta2int(lastTime-timeValue) < 0:
                return
            viewNum = i.find_all("td", "li_und")[
                0].text.strip().replace(",", "")
            voteNum = i.find_all("td", "li_und")[
                1].text.strip().replace(",", "")
            print("제목 : ", title, " 댓글수 : ", replyNum, " 시간 : ", timeValue.strftime("%Y/%m/%d, %H:%M:%S"),
                  " 추천수 : ", voteNum, " 조회수 : ", viewNum)


if __name__ == '__main__':
    getData()
