# -*- coding: utf-8 -*-
import datetime
import re
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisCrawlSpider
from LagouRedis.items import CategoryItem, InterviewItem, JobItem

class LagouTempSpider(RedisCrawlSpider):
    name = 'lagou_temp'
    redis_key = 'lagou_temp:start_url'
    # start_url = ['http://www.lagou.com/']

    rules = (
        Rule(LinkExtractor(allow=("zhaopin/.*",)), callback='parse_category', follow=True),
        Rule(LinkExtractor(allow=("jobs/\d+.html")), callback='parse_job', follow=True),
    )

    def parse_category(self, response):
        print('categoryurl', response.url)
        item = CategoryItem()
        item_con_list = response.css('ul.item_con_list > li')
        for li in item_con_list:
            item['category'] = re.search('zhaopin/(.*?)/', response.url).group(1)
            item['positionid'] = li.css('li::attr(data-positionid)').extract_first()
            item['positionname'] = li.css('li::attr(data-positionname)').extract_first()
            item['company'] = li.css('li::attr(data-company)').extract_first()
            item['companyid'] = li.css('li::attr(data-companyid)').extract_first()
            item['salary'] = li.css('li::attr(data-salary)').extract_first()
            publish_time = li.css('div.position > div.p_top > span::text').extract_first()
            item['publish_time'] = handle_time(publish_time)
            item['labels'] = ','.join(li.css('div.list_item_bot > div.li_b_l > span::text').extract())
            acquire = li.css('li > div.list_item_top > div.position > div.p_bot > div').extract()
            acquire = re.search(r'-->(.* .*)\\n', str(acquire)).group(1)
            item['acquire_year'] = acquire.split('/')[0].strip()
            item['acquire_edu_bg'] = acquire.split('/')[1].strip()
            item['update_time'] = str(datetime.datetime.now()).split('.')[0]
            yield item


    def parset_interview(self, response):
        item = InterviewItem()
        pass


    def parse_job(self, response):
        print('joburl', response.url)
        item = JobItem()
        jobid = re.search('/(\d+).html', response.url).group(1)
        item['jobid'] = jobid
        item['jobname'] = response.css('div.position-content-l > div::attr(title)').extract_first()
        item['jobcompanyname'] = response.css('div.job-name > div.company::text').extract_first()
        item['jobadvantage'] = response.css('#job_detail > dd.job-advantage > p::text').extract_first()
        jobcontent = response.css('#job_detail > dd.job_bt > div > p::text').extract()
        jobcontent = handle_text(jobcontent)
        item['jobreposibilit'] = jobcontent[0]
        item['jobacquire'] = jobcontent[1]
        jobsite = response.xpath('//*[@id="job_detail"]/dd[3]/div[1]/a/text()').extract()[:-2]
        jobsite_2 = response.xpath('//*[@id="job_detail"]/dd[3]/div[1]/text()').extract()
        jobsite.extend(jobsite_2)
        item['jobsite'] = handle_addr(jobsite)
        item['update_time'] = str(datetime.datetime.now()).split('.')[0]
        return item


# 拼接多行内容
def handle_text(text_list):
    filter_list = []
    inslice = 0
    num = 0
    for each in text_list:
        if len(each) < 6:
            inslice = num
        filter_list.append(each.strip())
        num += 1
    resp = ''.join(filter_list[1:inslice-1])
    acqu = ''.join(filter_list[inslice+1:])
    return [resp, acqu]



# 去除多余信息拼接地址
def handle_addr(text_list: list):
    filter_list = []
    for each in text_list:
        if len(each) > 1 and '\n' not in each:
            each = each.strip()
            filter_list.append(each)
    return ''.join(filter_list)


def handle_time(text):
    if text is None:
        return
    currect_datetime = datetime.datetime.now()
    if '天' in text:
        day = re.search('(\d+)天', text).group(1)
        date_time = currect_datetime - datetime.timedelta(days=int(day))
        return str(date_time).split('.')[0]
    return text
