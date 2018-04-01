# -*- coding:utf-8 -*-
import datetime
import json
import time
import os
import sys
import redis
import requests
import argparse

r = redis.StrictRedis(host='101.132.73.130', password='xxf99311')

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append('/home/barnett/anaconda3/bin/')


#-------------------------------------------Params Config----------------------------------------#
address = ['39.108.175.25', '101.132.73.130']
port = 6800
project_name = 'LagouRedis'
spider_name = 'lagou_temp'
redis_key = 'lagou_temp:start_url'
start_url = 'https://www.lagou.com'
# deploys = ['lagou_liserver', 'lagou_myserver']
#-------------------------------------------Params Config----------------------------------------#


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


def run(category, _addr, data=None):
    if data is None:
        resp = requests.get(category[0].format(addr=_addr, port=port))
    elif category[1] == 'get':
        resp = requests.get(category[0].format(addr=_addr, port=port, project=data))
    else:
        resp = requests.post(category[0].format(addr=_addr, port=port), data=data)
    return resp


def add_key(key=redis_key, url=start_url):
    r.lpush(key, url)


def flushdb():
    r.flushall()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="""It is used for interacting to scrapyd server. Before starting use this python script, there are 
                        some parameters you should set in the source code(this file) as follows:
                          address: list, containing your IP addresses of scrapyd;
                          port: int, your server port of scrapyd;
                          project_name: str, your project name;
                          spider_name: str, you spider name;
                          redis_key: str, redis key to start spider;
                          start_url: str, your target website.
                """
    )
    parser.add_argument('-a', '--addr',
                        help="the number of IP address, default 1",
                        type=int, choices=[i+1 for i in range(len(address))], default=1)
    parser.add_argument('-la', '--listaddr',
                        help="list IP address we can use, you can add yourself IP address by modifying source code.", action="store_true")
    parser.add_argument('-s', '--status', help="show daemon status.", action="store_true")
    parser.add_argument('-S', '--shcedule', help="shcedule the project.", action="store_true")
    parser.add_argument('-C', '--cancel', help="cancel project, it needs paramster jobid.", type=str)
    parser.add_argument('-lp', '--listproject', help='list project.', action='store_true')
    parser.add_argument('-lv', '--listversion', help='list version.', action='store_true')
    parser.add_argument('-ls', '--listspider', help='list spider.', action='store_true')
    parser.add_argument('-lj', '--listjobs', help='list job.', action='store_true')
    parser.add_argument('-dv', '--delversion', help='list version.', action='store_true')
    parser.add_argument('-dp', '--delproject', help='list project.', action='store_true')
    parser.add_argument('--flushdb', help="flush redis.", action='store_true')
    parser.add_argument('-ak', '--addkeys', help="add start_url into redis.", action='store_true')
    args = parser.parse_args()

    if args.listaddr:
        num = 1
        for i in address:
            print('IP address[%s]: ' % num, address[num - 1])
            num += 1
        print('default chocie addr num: ', 1)
    if args.addr:
        num = 1
        if not args.listaddr:
            for i in address:
                print('IP address[%s]: ' % num, address[num - 1])
                num += 1
            print("choose addr: ", address[args.addr - 1])
        else:
            pass
    if args.status:
        status = run(daemon_status, _addr=address[args.addr - 1])
        print('status: ', status.text)
    if args.shcedule:
        run_result = run(schedule, data={'project': project_name, 'spider': spider_name}, _addr=address[args.addr - 1])
        print(run_result.text)
    if args.cancel:
        cancelProject = run(cancel, data={'project': project_name, 'job': args.cancel}, _addr=address[args.addr - 1])
        print('cancel', cancelProject)
    if args.listproject:
        projects = run(list_projects, _addr=address[args.addr - 1])
        print('projects: ', projects.text)
    if args.listversion:
        versions = run(list_versions, data=project_name, _addr=address[args.addr - 1])
        print('versions: ', versions.text)
    if args.listspider:
        spiders = run(list_spiders, data=project_name, _addr=address[args.addr - 1])
        print('spiders: ', spiders.text)
    if args.listjobs:
        jobs = run(list_jobs, data=project_name, _addr=address[args.addr - 1])
        text = json.loads(jobs.text)
        for key in text:
            if not isinstance(text[key], list):
                print(key, ': ', text[key])
            else:
                print(key + ':')
                for each in text[key]:
                    if isinstance(each, dict):
                        try:
                            for a in each:
                                print('    ', a, ': ', each[a])
                                if a == 'start_time':
                                    start_time = each[a].split('.')[0]
                                if a == 'end_time':
                                    end_time = each[a].split('.')[0]
                            d1 = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
                            d2 = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                            total_time = d1 - d2
                            print('    ', 'total_time : ', total_time)
                        except:
                            pass
                    else:
                        print('    ', each)
                    print('    ', '-' * 45)
    if args.delproject:
        delProject = run(del_project, data={'project': project_name}, _addr=address[args.addr - 1])
        print('del:', delProject.text)
    if args.flushdb:
        while True:
            get = input('Are you sure to flush redis database(y/n): ')
            if get == 'y':
                flushdb()
                print('flushdb')
                break
            elif get == 'n':
                print('You canceled')
                break
            else:
                print("Please input y or n")
    if args.addkeys:
        add_key(redis_key, start_url)
        print('lpush %s %s' % (redis_key, start_url))

