# coding=utf-8
from common.util import *

WEBSITES = ["https://www.forbo.com/flooring/zh-cn/pib3mg"]

# 福尔波的新闻没有时间，所以不支持按时间下载，只能全量下载，所幸它的新闻比较少


def download_with_url(curr_url):
    soup = get_html_soup(curr_url)
    h4_list = soup.find_all("h4", "title")
    div_list = soup.find_all("div", "content")
    for i in range(0, len(h4_list)):
        h4 = h4_list[i]
        div = div_list[i]
        title = title_format(h4.a["title"].encode("utf-8"))
        intro = div.text.encode("utf-8")
        context = intro_format(intro)
        save_to_file("福尔波", "未知时间", title, "", context)


def download_all():
    for curr_url in WEBSITES:
        print "正在爬取网站：【" + curr_url + "】"
        download_with_url(curr_url)


