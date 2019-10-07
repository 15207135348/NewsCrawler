# coding=utf-8
import os
import re
from bs4 import BeautifulSoup
import requests

PARSE = "html.parser"
# 保存文件的根路径
ROOT_PATH = "." + os.sep + "data"


def get_html_soup(url, encode='utf-8'):
    try:
        response = requests.get(url)
        response.encoding = encode
        text = response.text
    except Exception as e:
        print(e, "please check your network situation")
        return None
    return BeautifulSoup(text, PARSE)


def save_to_file(website, date, title, info, context):
    print "成功从【" + website + "】下载新闻: " + title
    d = ROOT_PATH + os.sep + date + os.sep + website
    filename = d + os.sep + title + '.txt'
    if not os.path.exists(d):
        os.makedirs(d)
    f = open(filename, 'w')
    string = title + '\n\n' + info + '\n\n' + context
    f.write(string)
    f.flush()
    f.close()


def filter_tags(html_str):
    # 先过滤CDATA
    re_cdata = re.compile('//<!\[CDATA\[[^>]*//\]\]>', re.I)  # 匹配CDATA
    re_script = re.compile('<\s*script[^>]*>[^<]*<\s*/\s*script\s*>', re.I)  # Script
    re_style = re.compile('<\s*style[^>]*>[^<]*<\s*/\s*style\s*>', re.I)  # style
    re_br = re.compile('<br\s*?/?>')  # 处理换行
    re_h = re.compile('</?\w+[^>]*>')  # HTML标签
    re_comment = re.compile('<!--[^>]*-->')  # HTML注释
    s = re_cdata.sub('', html_str)  # 去掉CDATA
    s = re_script.sub('', s)  # 去掉SCRIPT
    s = re_style.sub('', s)  # 去掉style
    s = re_br.sub('\n', s)  # 将br转换为换行
    s = re_h.sub('', s)  # 去掉HTML 标签
    s = re_comment.sub('', s)  # 去掉HTML注释
    # 去掉多余的空行
    blank_line = re.compile('\n+')
    s = blank_line.sub('\n', s)
    s = replace_char_entity(s)  # 替换实体
    return s


def replace_char_entity(html_str):
    char_entities = {'nbsp': ' ', '160': ' ',
                     'lt': '<', '60': '<',
                     'gt': '>', '62': '>',
                     'amp': '&', '38': '&',
                     'quot': '"', '34': '"', }
    re_char_entity = re.compile(r'&#?(?P<name>\w+);')
    sz = re_char_entity.search(html_str)
    while sz:
        key = sz.group('name')  # 去除&;后entity,如&gt;为gt
        try:
            html_str = re_char_entity.sub(char_entities[key], html_str, 1)
            sz = re_char_entity.search(html_str)
        except KeyError:
            # 以空串代替
            html_str = re_char_entity.sub('', html_str, 1)
            sz = re_char_entity.search(html_str)
    return html_str


def title_format(title):
    return filter_tags(title).replace("\\", "-").replace("/", "-")


def intro_format(intro):
    context = ""
    for line in intro.splitlines():
        line = line.strip()
        if line == '':
            continue
        context = context + line + '\n'
    return context
