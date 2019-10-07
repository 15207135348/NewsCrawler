# coding=utf-8
import datetime

from common.util import *

WEBSITES = ["http://www.chinajinyiyuan.com/nav/11.html"]
ROOT_WEBSITE = "http://www.chinajinyiyuan.com"


def download_with_url(curr_url, start_date, stop_date):
    soup = get_html_soup(curr_url)
    ul = BeautifulSoup(str(soup.find("ul", "news_two_ul")), PARSE)
    li_list = ul.find_all("li")
    for li in li_list:
        # 日期
        date = li.div.p.text.encode("utf-8").replace('\n', '').replace('\t', '').replace(' ', '')
        # 如果日期比stop_date大，那么忽略这条新闻
        if date > stop_date:
            print "忽略" + date
            continue
        # 如果日期比start_date小，说明下载完毕了
        if date < start_date:
            return True
        # 标题
        title = title_format(li.div.a.img["alt"].encode("utf-8"))
        # 链接
        href = ROOT_WEBSITE + li.div.a["href"].encode("utf-8")
        # 正文
        intro = get_html_soup(href)
        patten = re.compile("c_news_detail*")
        intro = intro.find("div", patten).text.encode("utf-8")
        context = intro_format(intro)
        # 保存
        save_to_file("金亿源", date, title, "", context)
    # 没有下载完毕，需要获取下一页继续下载
    return False


def download(start_date, stop_date):
    for curr_url in WEBSITES:
        print "正在爬取网站：【" + curr_url + "】"
        download_with_url(curr_url, start_date, stop_date)


def download_today():
    today = datetime.date.today().strftime("%Y-%m-%d")
    download(today, today)

