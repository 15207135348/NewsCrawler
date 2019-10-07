# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["https://hao.pvc123.com/news-5.html", "https://hao.pvc123.com/news-1.html",
            "https://hao.pvc123.com/news-2.html", "https://hao.pvc123.com/news-4.html"]
ROOT_WEBSITE = "https://hao.pvc123.com"


def next_page(current_url):
    soup = get_html_soup(current_url)
    return ROOT_WEBSITE + soup.find("a", "loadMore")["href"].encode("utf-8")


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url)
    ul = BeautifulSoup(str(soup.find("ul", "news")), PARSE)
    li_list = ul.find_all('li')
    for e in li_list:
        li = BeautifulSoup(str(e), PARSE)
        # 获取新闻链接
        href = ROOT_WEBSITE + li.a["href"].encode('utf-8').strip()
        # 打开链接
        new_page = BeautifulSoup(str(get_html_soup(href)), PARSE)
        head = new_page.find("div", "head")
        content_restore = new_page.find("div", "content restore")
        # 日期
        date = head.span.text.encode("utf-8")[0:10]
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 标题
        title = head.h2.text.encode("utf-8")
        # 基本信息
        info = head.text.encode('utf-8').replace(title, "")
        # 新闻的主要内容
        intro = content_restore.text.encode('utf-8')
        context = intro_format(intro)
        # 保存
        save_to_file("环球塑化", date, title, info, context)
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
