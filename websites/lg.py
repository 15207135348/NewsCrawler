# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["http://www.lghausyschina.com/site/news"]
ROOT_WEBSITE = "http://www.lghausyschina.com"


def all_pages():
    pages = []
    soup = get_html_soup(WEBSITES[0])
    div = BeautifulSoup(str(soup.find("div", "newsyear")), PARSE)
    all_a = div.find_all("a")
    for a in all_a:
        href = ROOT_WEBSITE + a["href"].encode("utf-8")
        pages.append(href)
    return pages


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url)
    div_list = soup.find_all("div", "picture-item__inner")
    for div in div_list:
        # 日期
        date = div.p.text.encode("utf-8")
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 标题
        title = title_format(div.h3.a.text.encode("utf-8"))
        # 链接
        href = ROOT_WEBSITE + '/' + div.h3.a["href"].encode("utf-8")
        # 内容
        intro = get_html_soup(href).find("div", "pagetext").text.encode("utf-8")
        context = intro_format(intro)
        # 保存
        save_to_file("LG", date, title, "", context)
    # 没有下载完毕，需要获取下一页继续下载
    return False


def download(start_date, stop_date):
    url_list = all_pages()
    for curr_url in url_list:
        print "正在爬取网站：【" + curr_url + "】"
        download_with_url(curr_url, start_date, stop_date)


def download_today():
    today = datetime.date.today().strftime("%Y-%m-%d")
    download(today, today)
