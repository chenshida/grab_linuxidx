#! /usr/bin/python
# -*- coding: utf-8 -*-

from bin.HTTPAuthorization import HTTPAuthorization
from bin.PageHandler import PageHandler
import re
import os

# set default coding
# import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

# set the directory
cwd = os.getcwd()
new_dir = cwd + '/linuxidc'
try:
    os.chdir(new_dir)
except OSError as e:
    os.mkdir(new_dir)
    os.chdir(new_dir)
finally:
    print(os.getcwd())

# 根目录网址及用户名密码
url = 'https://linux.linuxidc.com'
username = 'www.linuxidc.com'
password = 'www.linuxidc.com'

# 创建授权header
httpauthorization = HTTPAuthorization(username, password)
authheader = httpauthorization.gen_authheader()

url_page = PageHandler(url,authheader)

try:
    url_page_text = url_page.read_page()
    print('\n===================================\n')
    url_page.analysis_page()
except IOError as e:
    print(e)

if __name__ == '__main__':
    pass
