# encoding=utf-8

import re
import csv
import requests
from bs4 import BeautifulSoup
import pandas
from pandas import read_csv


headers = {
    "Connection": "keep-alive",
    "Cache-Control": "max-age=0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36",
    "Accept-Encoding": "gzip,deflate,sdch",
    "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.6,en;q=0.4,zh-TW;q=0.2",
}


# rootPath = '/Users/floyd/Desktop/Research/NER-CRF/cctner/'
rootPath = ''

class Radical(object):
    dictionary_filepath = rootPath + 'sources/xinhua.csv'
    baiduhanyu_url = 'http://hanyu.baidu.com/zici/s?ptype=zici&wd=%s'

    def __init__(self):
        self.dictionary = read_csv(self.dictionary_filepath)

    def get_radical(self,word):
        if word in self.dictionary.char.values:
            return self.dictionary[self.dictionary.char == word].radical.values[0]
        else:
            return self.get_radical_from_baiduhanyu(word)

    def get_radical_from_baiduhanyu(self,word):
        url = self.baiduhanyu_url % word
        print(url)
        try:
            r = requests.get(url)
            html = str(r.content, 'utf-8')
        except Exception as e:
            print('URL Request Error:', e)
            html = None

        if html == None:
            return None
        soup = BeautifulSoup(html, 'html.parser')
        li = soup.find(id="radical")
        radical = li.span.contents[0]

        if radical != None:
            self.dictionary = self.dictionary.append({'char': word, 'radical': radical}, ignore_index= True)
            self.dictionary.to_csv(self.dictionary_filepath, encoding = 'utf-8', index = False)

        return radical


if __name__ == '__main__':
    r = Radical()
    print(r.get_radical('铞'))
    print(r.get_radical('落'))
    # r.save()



    