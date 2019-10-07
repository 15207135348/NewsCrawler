# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["https://www.armstrongceilings.cn/commercial/zh-cn/press-releases.html"]
ROOT_WEBSITE = "https://www.armstrongceilings.cn"


def date_format(src):
    index = src.find("年")
    year = int(src[0: index])
    src = src[index:].replace("年", "")
    index = src.find("月")
    month = int(src[0: index])
    res = "{:0>4d}-{:0>2d}-{:0>2d}".format(year, month, 1)
    return res.encode("utf-8")


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url)
    li_list = soup.find_all("article", "content-link")
    for li in li_list:
        date = date_format(li.p.text.encode("utf-8"))
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 标题
        title = title_format(li.h5.a.text.encode("utf-8"))
        # 链接
        href = ROOT_WEBSITE + '/' + li.a["href"].encode("utf-8")
        # 正文
        intro = get_html_soup(href).find("article", id="stickywrapper").text.encode("utf-8")
        context = intro_format(intro)
        # 保存
        save_to_file("阿姆斯壮", date, title, "", context)
    # 没有下载完毕，需要获取下一页继续下载
    return False


def download(start_date, stop_date):
    for curr_url in WEBSITES:
        print "正在爬取网站：【" + curr_url + "】"
        download_with_url(curr_url, start_date, stop_date)


def download_today():
    today = datetime.date.today().strftime("%Y-%m-%d")
    download(today, today)

