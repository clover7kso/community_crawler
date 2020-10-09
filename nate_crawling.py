import re
import csv
from urllib.request import urlopen, Request
from bs4 import BeautifulSoup
from multiprocessing import Process, Queue, Manager

from datetime import date
from datetime import datetime
from datetime import time

# 시작 URL
BASE_URL = "https://pann.nate.com/talk/ranking?rankingType=life&page=1"


def getUrls():

    reqUrl = Request(BASE_URL, headers={'User-Agent': 'Mozilla/5.0'})
    html = urlopen(reqUrl)
    soup = BeautifulSoup(html, "html.parser")
    soup = soup.find("ul", "post_wrap")

    URLs = []
    for i in soup.find_all("li"):
        URLs.append("https://pann.nate.com"+i.find("a")["href"])
    return URLs


def getData(Urls):
    for i in Urls:
        reqUrl = Request(i, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(reqUrl)
        soup = BeautifulSoup(html, "html.parser")
        soup = soup.find("div", "view-wrap")

        title = soup.find("h4")['title']
        timeString = soup.find("span", "date").text.strip()
        timeValue = datetime.strptime(timeString, '%Y.%m.%d %H:%M')

        viewNum = soup.find("span", "count").text.strip().replace(
            "조회", "").replace(",", "")
        voteNum = soup.find("div", "updown f_clear").find(
            "span", "count").text.strip().replace(",", "")
        replyNum = soup.find("span", "num").find(
            "strong").text.strip().replace(",", "")

        print("제목 : ", title, " 댓글수 : ", replyNum, " 시간 : ", timeValue.strftime(
            "%Y/%m/%d, %H:%M:%S"), " 추천수 : ", voteNum, " 조회수 : ", viewNum)


if __name__ == '__main__':
    getData(getUrls())
