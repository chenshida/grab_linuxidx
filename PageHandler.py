#! /usr/bin/python
# -*- coding:utf-8 -*-

# import urllib2
import urllib
import urllib.request
import re
import os
from bs4 import BeautifulSoup

# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

filter_list = ["/", '切换', '.png', '吃豆人', '五子棋', '坦克大战', '中国象棋', '资源站', '文件名', '大小', '上传时间', 'Linux公社']

def filterNoUse(inputStr, filterItem):
    for item in filterItem:
        if item in inputStr:
            return True
    return False


class PageHandler:
    def __init__(self, url, authheader = None):
        print("create new page handler: ", url)
        self.url = url
        self.authheader = authheader
        # self.url_req = urllib2.Request(url)
        self.url_req = urllib.request.Request(url)
        self.cur_dir = os.getcwd()
        if self.authheader != None:
            self.url_req.add_header("Authorization", authheader)
            self.url_req.add_header("User-Agent", 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36')


    def open_page(self):
        # self.url_handler = urllib2.urlopen(self.url_req)
        self.url_handler = urllib.request.urlopen(self.url_req)


    def read_page(self):
        self.open_page()
        return self.url_handler.read()


    def download_page(self, url, text):
        download_page_handler = PageHandler(url, self.authheader)
        try:
            download_file = download_page_handler.read_page()
            with open(text, "wb") as code:
                code.write(download_file)
            pass
        except IOError as e:
            print(text, e, "\n download failed")
            pass

        print(text, 'downloaded')
        pass


    def analysis_page(self):
        self.page_soup = BeautifulSoup(self.read_page(),"html.parser")

        # find all link
        self.url_list = self.page_soup.find_all('a')
        # print("self.url_list: ", self.url_list)
        # link iteration
        link_url = None
        for link in self.url_list:
            # link_url = "http://linux.linuxidc.com" + link.get('href')
            # print("link.get('href'): ", link.get('href'))
            link_get = link.get('href')
            if link_get == "https://linux.linuxidc.com/" or link_get == "index.php":
                continue
            else:
                link_url = "https://linux.linuxidc.com" + "/" + link_get
                # print("nimei")
                # link_url = "https://linux.linuxidc.com/index.php"
            # link_url = self.url + link.get('href')

            # match directory
            regex_pattern = r'.\..'
            pattern = re.compile(regex_pattern)
            text = link.get_text()
            # print("text: ", text)
            text_match = re.findall(regex_pattern, text)
            # text_match = re.findall(pattern, text)

            # current directory has files
            if text_match:
                self.download_page(link_url, text)
            elif text == '[To Parent Directory]':
                pass
            elif filterNoUse(text, filter_list):
                print("text with no useful")
                pass
            else: # get a new page
                filter_list.append(text)
                self.create_dir(text)
                new_pagehandler = PageHandler(link_url, self.authheader)
                try:
                    new_pagehandler.analysis_page()
                except IOError as e:
                    print(text,e)
                    pass
                finally:
                    os.chdir(self.cur_dir)



    def create_dir(self, link_text):
        cwd = os.getcwd()
        new_dir = os.path.join(cwd, link_text)
        # print("new_dir: ", new_dir)

        try:
            os.chdir(new_dir)
        except OSError as e:
            # os.mkdir(new_dir)
            os.makedirs(new_dir)
            os.chdir(new_dir)
        finally:
            # print os.getcwd()
            pass


if __name__ == '__main__':
    pass
