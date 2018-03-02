# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class JobItem(scrapy.Item):
    ''' Job 信息 '''
    job_id = scrapy.Field()          # id
    job_detail_id = scrapy.Field()   # job detail id
    job_name = scrapy.Field()        # 职位名称
    job_url = scrapy.Field()         # 职位url
    review_percent = scrapy.Field()  # 反馈率
    company_name = scrapy.Field()    # 公司名称
    company_url = scrapy.Field()     # 公司网址
    job_salary = scrapy.Field()      # 职位月薪
    salary_min = scrapy.Field()      # 职位月薪Min
    salary_max = scrapy.Field()      # 职位月薪Max
    job_location = scrapy.Field()    # 工作地点
    job_date = scrapy.Field()        # 发布时间
    from_app = scrapy.Field()        # 来源APP
    create_time = scrapy.Field()     # 爬取时间


class JobDetailItem(scrapy.Item):
    ''' 职位详情 '''
    # 职位信息
    job_id = scrapy.Field()            # job id
    job_name = scrapy.Field()          # 职位名称
    job_url = scrapy.Field()           # job url
    job_tags = scrapy.Field()          # 标签
    job_salary = scrapy.Field()        # 月薪
    salary_min = scrapy.Field()        # 月薪Min
    salary_max = scrapy.Field()        # 月薪Max
    job_location = scrapy.Field()      # 工作地点
    job_date = scrapy.Field()          # 发布时间
    job_nature = scrapy.Field()        # 工作性质
    work_years = scrapy.Field()        # 工作经验
    work_years_min = scrapy.Field()    # 工作经验Min
    work_years_max = scrapy.Field()    # 工作经验Max
    min_degree = scrapy.Field()        # 最低学历
    ofer_members = scrapy.Field()      # 招聘人数
    job_cate = scrapy.Field()          # 职位类别
    job_skills = scrapy.Field()        # 职位要求
    # 公司信息
    company_name = scrapy.Field()      # 公司名称
    company_url = scrapy.Field()       # 公司网址
    company_nature = scrapy.Field()    # 公司性质
    company_size = scrapy.Field()      # 公司规模
    company_size_min = scrapy.Field()  # 公司规模Min
    company_size_max = scrapy.Field()  # 公司规模Max
    company_industry = scrapy.Field()  # 公司行业
    company_address = scrapy.Field()   # 公司地址
    company_intro = scrapy.Field()     # 公司简介
    #
    from_app = scrapy.Field()          # 来源APP
    create_time = scrapy.Field()       # 爬取时间
