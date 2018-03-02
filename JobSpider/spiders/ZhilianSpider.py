# -*- coding: utf-8 -*-

"""
爬取招聘网站工作信息。
框架：scrapy
"""

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import re
import time

from scrapy import Spider, Request, FormRequest
from scrapy.spider import CrawlSpider, Rule
from scrapy.linkextractor import LinkExtractor
from faker import Factory
from scrapy_splash import SplashRequest
# import urlparse
from JobSpider.items import JobItem, JobDetailItem

FACTORY = Factory.create() # 初始化生成器

class JobSpider(CrawlSpider):
    """ Zhilian Job Spider """
    name = "ZhilianSpider"
    allow_domains = [
        'sou.zhaopin.com',
        'jobs.zhaopin.com'
    ]

    """ url拼接 """
    joblocation = '选择地区'
    keyword = '大数据开发工程师'
    p = 1
    kt = 1                      # 1:职位名称; 2:公司名;
    isadv = 0
    sm = 0
    sortby = 0                  # 0:默认排序; 1:相关度; 2:首发日; 3: 最匹配;
    isfilter = 0
    # jobcategory  = 16000      # bj: 职位类别
    # in = 16000                # in:行业类别
    publish_date = 3            # pd: 1:今天; 2:最近3天; 3:最近一周; 4:最近一个月; 0:不限;
    url = 'http://sou.zhaopin.com/jobs/searchresult.ashx?' \
            'jl=%s&kw=%s&p=%d&isadv=%d&sb=%d&isfilter=%d&pd=%d' \
            %(joblocation, keyword, p, isadv, sortby, isfilter, publish_date)
    # print '========================= %s' %url
    start_urls = [
        # 'http://jobs.zhaopin.com/397133287250062.htm'
        url
    ]

    rules = (
        # Rule(LinkExtractor(allow=r"/jobs/searchresult.ashx$")),
        Rule(LinkExtractor(allow=r"/jobs/searchresult.ashx\?.*?", restrict_xpaths="//div[@class='pagesDown']"), callback="parse_job", follow=True),
        Rule(LinkExtractor(allow=r"/\d+.htm$", restrict_xpaths="//div[@id='newlist_list_content_table']/table"), callback="parse_job_detail", follow=True),
        Rule(LinkExtractor(allow=r"/\d+.htm$"), callback="parse_job_detail", follow=False),
    )

    # headers = {
    #     'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    #     'Accept-Encoding': 'gzip, deflate, br',
    #     'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    #     'Connection': 'keep-alive',
    #     # 'Referer': 'http://ts.zhaopin.com/jump/index.html?sid=121113803&site=pzzhubiaoti1',
    #     # 'Host': '',
    #     'User-Agent': FACTORY.user_agent()
    # }

    # formdata = {
    #     'LoginName': 'h295203236@163.com',
    #     'Password': 'huangbiao123'
    # }

    def parse_job(self, response):
        """ 获取 job 信息 """
        for sel in response.xpath('//*[@id="newlist_list_content_table"]/table[position()>1]'):
            try:
                item = JobItem()
                # item = {}
                item['job_id'] = "".join(sel.xpath('tr[1]/td[@class="zwmc"]/input[@name="vacancyid"]/@data-monitor').extract()).split('|')[0]
                item['job_detail_id'] = item['job_id'].replace('C', '').replace('J', '').split('|')[0]
                item['job_name'] = "".join(sel.xpath('tr[1]/td[@class="zwmc"]/div/a/text()').extract())
                if item['job_name'] == '':
                    item['job_name'] = "".join(sel.xpath('tr[1]/td[@class="zwmc"]/div/a/b/text()').extract())
                item['job_url'] = "".join(sel.xpath('tr[1]/td[@class="zwmc"]/div/a/@href').extract())
                item['review_percent'] = "".join(sel.xpath('tr[1]/td[@class="fk_lv"]/span/text()').extract())
                item['company_name'] = "".join(sel.xpath('tr[1]/td[@class="gsmc"]/a/text()').extract())
                item['company_url'] = "".join(sel.xpath('tr[1]/td[@class="gsmc"]/a/@href').extract())
                item['job_salary'] = "".join(sel.xpath('tr[1]/td[@class="zwyx"]/text()').extract())
                # 处理月薪
                salaryObj1 = re.search(r'(\d+)\D+(\d+)', item['job_salary'])
                salaryObj2 = re.search(r'(\d+)', item['job_salary'])
                if salaryObj1:
                    item['salary_min'] = salaryObj1.group(1)
                    item['salary_max'] = salaryObj1.group(2)
                elif salaryObj2:
                    item['salary_min'] = salaryObj2.group(1)
                    item['salary_max'] = item['salary_min']
                else:
                    item['salary_min'] = 0
                    item['salary_max'] = 0
                item['job_location'] = "".join(sel.xpath('tr[1]/td[@class="gzdd"]/text()').extract())
                item['job_date'] = "".join(sel.xpath('tr[1]/td[@class="gxsj"]/span/text()').extract())
                if item['job_date'] == u"刚刚":
                    item['job_date'] = "1小时内"
                item['from_app'] = "zhilian"
                item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
                # print item
                yield item
            except Exception as ex:
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message

    def parse_job_detail(self, response):
        """ 抓取 job 详情信息 """
        print "================================================"
        # print response.body
        try:
            item = JobDetailItem()
            # 1.获取公司信息
            comany_info_dic = {
                u'公司规模': ['company_size', 'strong/text()'],
                u'公司性质': ['company_nature', 'strong/text()'],
                u'公司行业': ['company_industry', 'strong/a/text()'],
                u'公司主页': ['company_url', 'strong/a/text()'],
                u'公司地址': ['company_address', 'strong/text()']
            }
            item['job_url'] = response.url
            item['job_id'] = item['job_url'].split('/')[-1].split('.')[0]
            item['job_name'] = "".join(response.xpath('///body/div[@class="top-fixed-box"]/div[1]/div[1]/h1/text()').extract())
            item['company_name'] = "".join(response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/text()').extract())
            item['company_url'] = "".join(response.xpath('//div[@class="company-box"]/p[@class="company-name-t"]/a/@href').extract())
            # 公司其他信息
            for li in response.xpath('//div[@class="company-box"]/ul/li'):
                cname = li.xpath('span/text()').extract()
                if cname:
                    cname = cname[0].decode('utf-8').replace(' ', '').replace('：', '').replace(':', '').strip()
                    item[comany_info_dic[cname][0]] = "".join(li.xpath(comany_info_dic[cname][1]).extract()).strip()
            item['company_address'] = item['company_address'].replace('\r\n','').strip()
            # 处理公司规模
            szieObj1 = re.search(r'(\d+)\D+(\d+)', item['company_size'])
            szieObj2 = re.search(r'(\d+)', item['company_size'])
            if szieObj1:
                item['company_size_min'] = szieObj1.group(1)
                item['company_size_max'] = szieObj1.group(2)
            elif szieObj2:
                item['company_size_min'] = szieObj2.group(1)
                item['company_size_max'] = item['company_size_min']
            else:
                item['company_size_min'] = 0
                item['company_size_max'] = 0

            # 2.获取 job 基础信息
            base_info_dic = {
                u'职位月薪': ['job_salary', 'strong/text()'],
                u'工作地点': ['job_location', 'strong/text()'],
                u'发布日期': ['job_date', 'strong/span/text()'],
                u'工作性质': ['job_nature', 'strong/text()'],
                u'工作经验': ['work_years', 'strong/text()'],
                u'最低学历': ['min_degree', 'strong/text()'],
                u'招聘人数': ['ofer_members', 'strong/text()'],
                u'职位类别': ['job_cate', 'strong/a/text()']
            }
            for li in response.xpath('//div[@class="terminalpage-left"]/ul/li'):
                cname = li.xpath('span/text()').extract()
                if cname:
                    cname = cname[0].decode('utf-8').replace(' ', '').replace('：', '').replace(':', '').strip()
                    item[base_info_dic[cname][0]] = "".join(li.xpath(base_info_dic[cname][1]).extract()).strip()
            # 处理月薪
            salaryObj1 = re.search(r'(\d+)\D+(\d+)', item['job_salary'])
            salaryObj2 = re.search(r'(\d+)', item['job_salary'])
            if salaryObj1:
                item['salary_min'] = salaryObj1.group(1)
                item['salary_max'] = salaryObj1.group(2)
            elif salaryObj2:
                item['salary_min'] = salaryObj2.group(1)
                item['salary_max'] = item['salary_min']
            else:
                item['salary_min'] = 0
                item['salary_max'] = 0
            # 处理工作年限
            yearsObj1 = re.search(r'(\d+)\D+(\d+)', item['work_years'])
            yearsObj2 = re.search(r'(\d+)', item['work_years'])
            if yearsObj1:
                item['work_years_min'] = yearsObj1.group(1)
                item['work_years_max'] = yearsObj1.group(2)
            elif yearsObj2:
                item['work_years_min'] = yearsObj2.group(1)
                item['work_years_max'] = item['work_years_min']
            else:
                item['work_years_min'] = 0
                item['work_years_max'] = 0
            # 处理招聘人数
            offerObj = re.search(r'(\d+)', item['ofer_members'])
            if offerObj:
                item['ofer_members'] = offerObj.group(1)
            else:
                item['ofer_members'] = 0
            # 获取job tags
            item['job_tags'] = ";".join(response.xpath('//div[@class="welfare-tab-box"]/span/text()').extract())
            # 获取job需求
            item['job_skills'] = "".join(response.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[1]').extract()).replace("'",'"')
            # 获取公司简介
            item['company_intro'] = "".join(response.xpath('//div[@class="terminalpage-main clearfix"]/div[@class="tab-cont-box"]/div[2]').extract()).replace("'",'"')
            item['from_app'] = "zhilian"
            item['create_time'] = time.strftime('%Y-%m-%d %H:%M:%S')
            # print item
            yield item
        except Exception as ex:
            print "====================== error ======================"
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print message