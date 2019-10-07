# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["https://www.chinafloor.cn/news/attrlist-htm-a-h.html",
            "https://www.chinafloor.cn/news/attrlist-htm-a-o.html",
            "https://www.chinafloor.cn/news/list-1515.html",
            "https://www.chinafloor.cn/news/list-1958.html",
            "https://www.chinafloor.cn/news/list-1525.html",
            "https://www.chinafloor.cn/news/qiye/",
            "https://www.chinafloor.cn/news/list-1524.html",
            "https://www.chinafloor.cn/zt/"]
ROOT_WEBSITE = "https://www.chinafloor.cn"


def next_page(current_url):
    soup = get_html_soup(current_url)
    a_list = BeautifulSoup(str(soup.find("div", "db-page")), PARSE).find_all("a")
    for a in a_list:
        if a.text.encode('utf-8').strip() == "下一页":
            return a["href"].encode("utf-8")
    return None


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url)
    div = BeautifulSoup(str(soup.find("div", "db-news-list cf")), PARSE)
    dl_list = div.find_all('dl')
    for e in dl_list:
        dl = BeautifulSoup(str(e), PARSE)
        # 过滤掉广告
        if dl.dd is None or dl.dd.h2 is None or dl.dd.h2.a is None:
            continue
        # 标题
        title = title_format(dl.dd.h2.a["title"].encode("utf-8"))
        # 获取新闻链接
        href = dl.dd.h2.a["href"].encode("utf-8").strip()
        # 打开链接
        new_page = BeautifulSoup(str(get_html_soup(href)), PARSE)
        db_source = new_page.find("p", "db-source")
        # 基本信息
        info = db_source.text.encode('utf-8')
        # 日期
        date = db_source.span.text.encode('utf-8').strip()[0:10]
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 新闻摘要
        abstract = new_page.find("p", "db-lead").text.encode('utf-8')
        # 新闻的主要内容
        intro = new_page.find("div", "db-detail").text.encode('utf-8')
        context = intro_format(intro)
        # 保存
        save_to_file("中华地板", date, title, info, abstract + "\n\n" + context)
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
