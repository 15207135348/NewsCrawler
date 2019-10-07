
1. 程序的作用
    用于从8个PVC地板的网站中下载新闻

2. 使用的python版本是2.7
    需要先下载安装python2.7

3. 依赖的第三方库 requests、BeautifulSoup
    可以通过以下语句安装依赖库
    pip install requests
    pip install BeautifulSoup

4. 使用方法
    在main.py中运行即可
    提供三种方法，可以根据需要自行选择
    download_today下载今天的新闻
    download_by_date按日期范围下载新闻
    download_all下载所有新闻