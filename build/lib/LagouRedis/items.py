# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
from scrapy.downloadermiddlewares.redirect import RedirectMiddleware
import scrapy
from scrapy.loader.processors import MapCompose, Join

# 拼接多行内容
def handle_reposibilit(text_list: list):
    filter_list = []
    start = 0
    end = 2
    num = 0
    for each in text_list:
        if each == '职位描述':
            start = num
        if ';' not in each:
            each += ';'
        if len(each) == 0:
            end = num
            break
        filter_list.append(each)
        num += 1
    return filter_list[start+1:end-1]


def handle_acquire(text_list: list):
    filter_list = []
    start = 0
    end = 2
    num = 0
    for each in text_list:
        if each == '任职要求':
            start = num
        if ';' not in each:
            each += ';'
        if len(each) == 0:
            end = num
            break
        filter_list.append(each)
        num += 1
    return ''.join(filter_list[start+1:end-1])


# 去除多余信息拼接地址
def handle_addr(text_list: list):
    filter_list = []
    for each in text_list:
        if not len(each):
            each = each.strip()
            filter_list.append(each)
    return ''.join(filter_list[:-2])


class CategoryItem(scrapy.Item):
    category = scrapy.Field()
    positionid = scrapy.Field()
    positionname = scrapy.Field()
    company = scrapy.Field()
    companyid = scrapy.Field()
    salary = scrapy.Field()
    publish_time = scrapy.Field()
    labels = scrapy.Field(output_processor=Join(','))
    acquire_year = scrapy.Field()
    acquire_edu_bg = scrapy.Field()
    update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                    INSERT INTO lagoucategory(category, positionid, positionname, company, companyid, salary, 
                    publish_time, labels, acquire_year, acquire_edu_bg,update_time)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE salary=VALUES (salary), publish_time=VALUES (publish_time), update_time=VALUES (update_time);
                """

        params = (
            self['category'],
            self['positionid'], self['positionname'], self['company'], self['companyid'], self['salary'],
            self['publish_time'], self['labels'], self['acquire_year'], self['acquire_edu_bg'], self['update_time']
        )

        return insert_sql, params


class InterviewItem(scrapy.Item):
    companyid = scrapy.Field()
    id = scrapy.Field()
    userid = scrapy.Field()
    myscore = scrapy.Field()
    describescore = scrapy.Field()
    interviewscore = scrapy.Field()
    companyscore = scrapy.Field()
    comprehensivescore = scrapy.Field()
    content = scrapy.Field()
    positionname = scrapy.Field()
    companyname = scrapy.Field()
    createtime = scrapy.Field()
    isinterview = scrapy.Field()
    tagarray = scrapy.Field()
    update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
            INSERT INTO lagouinterview
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON DUPLICATE KEY UPDATE content=VALUES (content), tagarray=VALUES (tagarray), update_time=VALUES (update_time);
        """

        params = (
            self['companyid'],
            self['id'], self['userid'], self['myscore'], self['describescore'], self['interviewscore'], self['companyscore'],
            self['comprehensivescore'], self['content'],
            self['positionname'], self['companyname'], self['createtime'], self['isinterview'], self['tagarray'],
            self['update_time']
        )


        return insert_sql, params


class JobItem(scrapy.Item):
    jobid = scrapy.Field()
    jobname = scrapy.Field()
    jobcompanyname = scrapy.Field()
    jobadvantage = scrapy.Field()
    jobreposibilit = scrapy.Field()
    jobacquire = scrapy.Field()
    jobsite = scrapy.Field()
    update_time = scrapy.Field()

    def get_insert_sql(self):
        insert_sql = """
                INSERT INTO lagoujobs
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE jobsite=VALUES (jobsite), update_time=VALUES (update_time);
                """

        params = (
            self['jobid'], self['jobname'], self['jobcompanyname'],
            self['jobadvantage'], self['jobreposibilit'], self['jobacquire'], self['jobsite'], self['update_time']
        )

        return insert_sql, params
