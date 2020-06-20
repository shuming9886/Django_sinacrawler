#python3
# coding=utf-8
import requests
import json
from bs4 import BeautifulSoup
from urllib import parse
import re

import win_unicode_console
win_unicode_console.enable()

headers = {'User-Agent':'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6'}

url="https://m.weibo.cn/container/getIndex?type=wb&queryVal={}&luicode=10000011&lfid=106003type%3D1&title={}&containerid=100103type%3D2%26q%3D{}&page={}"

def crawler(keyword):
    result=[]
    pagecode=parse.quote(keyword)
    pagenum=10
    for i in range(1,pagenum):
        res = requests.get(url.format(pagecode, pagecode, pagecode, i))
        content = str(res.content, encoding="utf-8")
        thisdata = json.loads(content)      #str转dict
        for i in range(len(thisdata['data']['cards'][0]['card_group'])):
            # itemID = thisdata['data']['cards'][0]['card_group'][i]['mblog']['id']
            # itemCreate = thisdata['data']['cards'][0]['card_group'][i]['mblog']['created_at']
            # itemUser = thisdata['data']['cards'][0]['card_group'][i]['mblog']['user']['screen_name']
            itemText = thisdata['data']['cards'][0]['card_group'][i]['mblog']['text']
            if thisdata['data']['cards'][0]['card_group'][i]['mblog']['isLongText'] == True:
                itemText =thisdata['data']['cards'][0]['card_group'][i]['mblog']['longText']['longTextContent']
            # print(itemText)
            # print(type(itemText))
            soup = BeautifulSoup(itemText, "html.parser")
            itemTextPretty = ""
            for string in soup.stripped_strings:
                itemTextPretty += string
            # print(itemTextPretty)
            pattern=re.compile('\n+')                                   #去除文本中的换行符
            itemTextPretty=pattern.sub('',itemTextPretty)
            pattern1=re.compile(r'http://[a-zA-Z0-9.?/&=:]*', re.S)     #去除文本中的url链接
            itemTextPretty=pattern1.sub('',itemTextPretty)
            # pattern2=re.compile('👉|🙏|👏|😍|😊|💰|🎁|🤔|🌂|🙊|✌|👿|🍬|💓|🙏|↓|♡|💪|🎺|🌟',re.S)         #去除文本中的表情符号
            # itemTextPretty=pattern2.sub('',itemTextPretty)
            pattern3=re.compile('\[.*?\]',re.S)                         #去除文本中的表情[星星][心]
            itemTextPretty=pattern3.sub('',itemTextPretty)
            pattern4=re.compile('网页链接',re.S)
            itemTextPretty=pattern4.sub('',itemTextPretty)
            pattern5=re.compile('(#\w+#)',re.S)                         #去除主题
            itemTextPretty=pattern5.sub('',itemTextPretty)
            pattern6=re.compile('(@\w+)',re.S)                          #去除@
            itemTextPretty=pattern6.sub('',itemTextPretty)
            pattern7=re.compile('//:',re.S)
            itemTextPretty=pattern7.sub('',itemTextPretty)
            pattern8=re.compile('转发微博',re.S)
            itemTextPretty=pattern8.sub('',itemTextPretty)
            itemTextPretty.strip()
            if itemTextPretty!='' and itemTextPretty not in result:
                result.append(itemTextPretty)
    return result