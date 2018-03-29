# -*- coding:utf-8 -*-
import time
from scrapy.cmdline import execute
import os
import sys
import redis
import requests
import json
from scrapyd_api import ScrapydAPI

r = redis.StrictRedis(host='101.132.73.130', password='xxf99311')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('/home/barnett/anaconda3/bin/')


# addr = '101.132.73.130'
addr = '39.108.175.25'
port = 6800
project_name = 'LagouRedis'
spider_name = 'lagou_temp'
redis_key = 'lagou_temp:start_url'
start_url = 'https://www.lagou.com'
deploys = ['lagou_liserver', 'lagou_myserver']

daemon_status = ['http://{addr}:{port}/daemonstatus.json', 'get']
schedule = ['http://{addr}:{port}/schedule.json', 'post', ['project', 'spider']] # params : project spider
cancel = ['http://{addr}:{port}/cancel.json', 'post'] # params : project job
list_projects = ['http://{addr}:{port}/listprojects.json', 'get']
list_versions = ['http://{addr}:{port}/listversions.json?project={project}', 'get'] # params : project
list_spiders = ['http://{addr}:{port}/listspiders.json?project={project}', 'get'] # params : project
list_jobs = ['http://{addr}:{port}/listjobs.json?project={project}', 'get'] # params : project
del_version = ['http://{addr}:{port}/delversion.json', 'post', ['project', 'version']] # params : project version
del_project = ['http://{addr}:{port}/delproject.json', 'post', ['project']] # params : project


def scrapyd_client(deploy, project, version=str(time.time()).split('.')[0]):
    os.system('scrapyd-deploy {deploy} -p {project} --version {version}'.format(deploy=deploy[0], project=project, version=version))
    time.sleep(1)

def run(category, data=None):
    if data is None:
        resp = requests.get(category[0].format(addr=addr, port=port))
    elif category[1] == 'get':
        resp = requests.get(category[0].format(addr=addr, port=port, project=data))
    else:
        # if not isinstance(dict, type(data)):
        #     raise Exception('%s is a post request,pls make data a dict object, it has %d paramter(s)%s' % (category, len(category[2]), category[2]))
        resp = requests.post(category[0].format(addr=addr, port=port), data=data)
    return resp


def add_key(key=redis_key, url=start_url):
    r.lpush(key, url)


def flushdb():
    r.flushall()


if __name__ == '__main__':
    # scrapyd_client(deploys[0], project_name, 'v1.0.0')
    run(schedule, data={'project': project_name, 'spider': spider_name})
    status = run(daemon_status)
    projects = run(list_projects)
    versions = run(list_versions, project_name)
    spiders = run(list_spiders, project_name)
    jobs = run(list_jobs, project_name)
    print('status: ', status.text)
    print('projects: ', projects.text)
    print('versions: ', versions.text)
    print('spiders: ', spiders.text)
    print('jobs: ', jobs.text)

    # delProject = run(del_project, data={'project': 'project=LagouReids'})
    # delProject = run(del_project, data={'project': 'LagouRedis'})
    # cancelProject = run(cancel, data={'project': project_name, 'job': '42a23c84328e11e8851700163e0cb227'})
    # print('del:', delProject.text)
    # projects = run(list_projects)
    # print('projects: ', projects.text)
    # versions = run(list_versions, project_name)
    # print('versions: ', versions.text)

    # flushdb()

    # add_key(redis_key, start_url)
