# -*- coding: UTF-8 -*-
# __author__ = 'Sengo'
import re
from bs4 import BeautifulSoup

regex_cache = {}


def search(text, regex):
    regexcmp = regex_cache.get(regex)
    if not regexcmp:
        regexcmp = re.compile(regex)
        regex_cache[regex] = regexcmp
    return regexcmp.search(text)


# XSS白名单
VALID_TAGS = {'br': {}}


def parsehtml(html):
    if not html:
        return ""
    html = str(html).replace("</p>", "<br/>")
    soup = BeautifulSoup(html, "lxml")
    for tag in soup.findAll(True):
        if tag.name not in VALID_TAGS:
            tag.hidden = True
        else:
            attr_rules = VALID_TAGS[tag.name]
            for attr_name, attr_value in tag.attrs:
                # 检查属性类型
                if attr_name not in attr_rules:
                    del tag[attr_name]
                    continue

                # 检查属性值格式
                if not search(attr_value, attr_rules[attr_name]):
                    del tag[attr_name]

    return soup.renderContents()


