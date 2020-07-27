from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
import random
import  requests

def get_html_text(url, code='utf-8'):
    """get html source code"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
               '(KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        response.encoding = code
        return response.text
    except requests.exceptions.RequestException:
        return ''


with open('yiqing100.txt', 'w', encoding='utf-8') as f:
    homepage = 'https://www.douban.com/gallery/topic/125548/?target_type=gallery_topic&target_id=125548&from=singlemessage&dt_platform=com.douban.activity.wechat_friends&dt_dapp=1'
    soup = BeautifulSoup(get_html_text(homepage), 'html.parser')
    div = soup.find('div', id = 'topic-items')
    topics = div.find('div')
    for topic in topics('div', attrs={'class':'topic-item item-status'}):

        comments = topic.find('pre', attrs={'class':'status-full hide'})
        try:
            btn = topic.find('div', attrs={'item-action'})
            good = btn.find('span')
        except IndexError:
            good = '无评分'
        try:
            count = topic.find('div', attrs={'class':'item-state'})
            response = count.find('a', attrs={'class':'conmments-count'})
        except IndexError:
            response = '无评论'
        f.write(f'{good:6}\t{response:20}\t{comments:3000}\n')

