# coding=utf-8
import datetime
from websites import lg, da_ju_long, huan_qiu_su_hua, fu_er_bo, armstrong, hua_jing, jin_yi_yuan
from websites import zhong_hua_di_ban


def download_today():
    """
    下载今天的新闻
    """
    armstrong.download_today()
    da_ju_long.download_today()
    hua_jing.download_today()
    jin_yi_yuan.download_today()
    lg.download_today()
    fu_er_bo.download_all()
    huan_qiu_su_hua.download_today()
    zhong_hua_di_ban.download_today()


def download_by_date(start_date, stop_date):
    """
    根据开始日期和结束日期下载新闻
    :param start_date: 2019-09-29
    :param stop_date: 2019-10-03
    :return:
    """
    armstrong.download(start_date, stop_date)
    da_ju_long.download(start_date, stop_date)
    hua_jing.download(start_date, stop_date)
    jin_yi_yuan.download(start_date, stop_date)
    lg.download(start_date, stop_date)
    fu_er_bo.download_all()
    huan_qiu_su_hua.download(start_date, stop_date)
    zhong_hua_di_ban.download(start_date, stop_date)


def download_all():
    """
    下载到今天为止所有的新闻，！！！可能会花费很长时间！！！
    :return:
    """
    start_date = "0000-00-00"
    today = datetime.date.today().strftime("%Y-%m-%d")
    download_by_date(start_date, today)


if __name__ == '__main__':
    """
    程序启动的入口
    :return:
    """
    download_today()
