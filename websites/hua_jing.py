# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["http://www.hjfloors.cn/news"]
ROOT_WEBSITE = "http://www.hjfloors.cn"


def next_page(current_url):
    soup = get_html_soup(current_url, 'gb2312')
    page_list = BeautifulSoup(str(soup.find("ul", id="page_area")), PARSE).find_all('li')
    for page in page_list:
        if page.text.encode('utf-8') == "下一页":
            if current_url.endswith(".html"):
                index = current_url.rfind("/")
                current_url = current_url[0: index]
            return (current_url + '/' + page.a["href"]).encode("utf-8")
    return None


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url, 'gb2312')
    ul = BeautifulSoup(str(soup.find("div", "news").ul), PARSE)
    li_list = ul.find_all('li')
    for e in li_list:
        li = BeautifulSoup(str(e), PARSE)
        # 获取日期
        date = li.find('span').text.encode("utf-8")
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 获取title
        a = li.find_all("a")[1]
        title = a.text.encode('utf-8')
        # 获取新闻链接
        href = ROOT_WEBSITE + "/" + a["href"].encode('utf-8')
        # 打开链接
        new_page = BeautifulSoup(str(get_html_soup(href, 'gb2312')), PARSE)
        # 基本信息
        info = new_page.find("div", "zuozhe").text.encode('utf-8')
        # 新闻的主要内容
        intro = new_page.find("div", "tian_a").text.encode('utf-8')
        context = intro_format(intro)
        # 新闻的关键字
        keywords = new_page.find("div", "content_n_pn").text.encode('utf-8')
        # 保存
        save_to_file("华静", date, title, info, context + "\n\n" + keywords)
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
