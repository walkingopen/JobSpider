# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
import pymysql.cursors
from items import JobItem, JobDetailItem

class JobSpiderMongoDBPipeline(object):
    """ Save Job into mongo. """
    def __init__(self):
        client = pymongo.MongoClient("localhost", 27017)
        db = client["Job"]
        self.Job_ZL = db["Job_ZL"]

    def process_item(self, item, spider):
        """ 插入MongoDB """
        print '============================'
        if isinstance(item, JobDetailItem):
            print 'JobInfoItem True'
            try:
                # print item
                self.Job_ZL.insert(dict(item))
            except Exception as ex:
                print "========================= ERROR ==========================="
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                print "========================= ERROR ==========================="

        return item

class JobSpiderMysqlPipeline(object):
    """ Save Job into mysql. """
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                                          user='root',
                                          password='root123',
                                          db='MyJob',
                                          charset='utf8mb4',
                                          cursorclass=pymysql.cursors.DictCursor)

    def process_item(self, item, spider):
        """ 插入MySQL """
        print '============================'
        isSave = False
        table_name = ""
        int_attrs = []
        primary_key = ""
        if isinstance(item, JobItem):
            print 'JobItem True'
            table_name = "Job"
            primary_key = "job_id"
            int_attrs = [ 'salary_min', 'salary_max', 'job_detail_id' ]
            fields = JobItem.fields.keys()
            isSave = True
        elif isinstance(item, JobDetailItem):
            print 'JobDetailItem True'
            table_name = "JobDetail"
            primary_key = "job_id"
            int_attrs = [ 'salary_min', 'salary_max', 'work_years_min', 'work_years_max', 'ofer_members' ]
            fields = JobDetailItem.fields.keys()
            isSave = True
        if isSave:
            try:
                id = item[primary_key]
                with self.connection.cursor() as cursor:
                    sql_select = """select * from `%s` where `%s`='%s'""" %(table_name,primary_key,id)
                    count_rows = cursor.execute(sql_select)
                    if count_rows > 0:
                        print "============= haha this row data is already in database. =============="
                    else:
                        fields_sql = "`" + "`, `".join(fields) + "`"
                        values_sql = ""; i = 0
                        for attr in fields:
                            i += 1; sp = ", "
                            if i == 1:
                                sp = ""
                            if attr in int_attrs:
                                values_sql += sp + item[attr]
                            else:
                                values_sql += sp + "'" + item[attr] + "'"
                        sql_insert = """insert into `%s`(%s) values(%s)""" %(table_name,fields_sql,values_sql)
                        print sql_insert
                        # print sql_insert
                        cursor.execute(sql_insert)
                        self.connection.commit()
            except Exception as ex:
                print "========================= ERROR ==========================="
                template = "An exception of type {0} occurred. Arguments:\n{1!r}"
                message = template.format(type(ex).__name__, ex.args)
                print message
                print sql_select
                print "========================= ERROR ==========================="
            finally:
                # cursor.close()
                # self.connection.close()
                pass

        return item

    def __del__(self):
        self.connection.close()
