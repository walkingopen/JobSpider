# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html

import settings
from scrapy import signals
from scrapy.http import Request, FormRequest, HtmlResponse
import WebKit
# import jswebkit
# import gtk

class WebkitDownloader(object):
    '''
    由于很多页面含有js动态插入，所以这里定义一个Webkit下载器；
    等待 js 加载完成才进行下载。
    '''
    # def process_request(self, request, spider):
    #     if spider.name in settings.WEBKIT_DOWNLOADER:
    #         if isintance(request, FormRequest):
    #             webview = WebKit.webview
    #             webview.connect('load-finished', lambda v, f: gtk.main_quit())
    #             webview.load_uri(request.url)
    #             gtk.main()