# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["http://www.pvc66.cn/news/gsxw", "http://www.pvc66.cn/news/zhxx/", "http://www.pvc66.cn/news/hyxw/"]


def next_page(current_url):
    soup = get_html_soup(current_url)
    page_list = BeautifulSoup(str(soup.find("div", "pagelist")), PARSE)
    for page in page_list.find_all('li'):
        if page.text.encode('utf-8') == "下一页":
            if current_url.endswith(".html"):
                index = current_url.rfind("/")
                current_url = current_url[0: index]
            return (current_url + '/' + page.a["href"]).encode("utf8")
    return None


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url)
    ul = BeautifulSoup(str(soup.find("ul", "news_list mt20")), PARSE)
    li_list = ul.find_all('li')
    for e in li_list:
        li = BeautifulSoup(str(e), PARSE)
        # 获取日期
        temp = BeautifulSoup(str(li.find('span')), PARSE).text
        day = temp[0:2]
        year_month = temp[2:]
        date = (year_month + '-' + day).encode('utf-8')
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 获取title
        title = title_format(li.div.a["title"].encode('utf-8'))
        # 获取新闻链接
        href = li.div.a["href"]
        new = BeautifulSoup(str(get_html_soup(href).find("div", "news_show")), PARSE)
        # 新闻的基本信息
        info = new.find("div", "info").text.encode('utf-8')
        # 新闻的主要内容
        intro = new.find("div", "intro").text.encode('utf-8').replace('\t', '')
        context = intro_format(intro)
        save_to_file("大巨龙", date, title, info, context)
    # 没有下载完毕，需要获取下一页继续下载
    return False


def download(start_date, stop_date):
    for website in WEBSITES:
        curr_url = website
        while curr_url is not None:
            print "正在爬取网站：【" + curr_url + "】"
            ok = download_with_url(curr_url, start_date, stop_date)
            # 如果下载完毕，退出下载
            if ok:
                break
            # 否则，获取下一页继续下载
            curr_url = next_page(curr_url)


def download_today():
    today = datetime.date.today().strftime("%Y-%m-%d")
    download(today, today)
