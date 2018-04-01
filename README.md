# LagouRedis
#### 简介

​	使用scrapy框架和scrapy-redis组件进行**分布式全网**爬取lagou网站的职位信息。另外还写了一个**[LagouSpider](https://github.com/Barnettxxf/LagouSpider)**项目，使用scrapy写的定向爬取拉勾网职位信息的。

​	爬取字段分为两部分职位信息和招聘信息。

​	职位信息包含以下字段：jobid(职位ID),  jobname(职位名称),  jobcompanyname(职位公司名称),  jobadvantage(职位优势), jobresponsibility(职位职责), jobacquire(职位需求), jobsite(工作地址), updatetime(更新时间)等八个字段。

​	招聘信息包含以下字段：category(职位类别), positionid(职位ID), positionname(职位名称), company(公司名), companyid(公司ID), salary(工资), publishtime(发布时间), labels(标签), acquire_year(工作经验要求), acquire_edu_bg(学历要求), update_time(更新时间)等十一个字段。



## Requirements

​	Ubuntu 17.10

​	python 3.6 （anaconda3）

​	pymysql==0.8.0

​	redis==2.10.6

​	scrapy_redis==0.6.8

​	Scrapy==1.5.0

​	scrapyd

​	scrapyd-client

​	以上第三方库可以使用requirements直接安装，`pip install -r requirements`, 即可配置python环境需求，此外还需要用到MySQL数据库和Redis数据库。



## 使用方法

#### 配置scrapy.cfg

> ```
> [deploy:localspider]
> url = http://localhost:6800/
> project = LagouReids
> username = barnett
> password = 123456
>
> [deploy:DeloyName]
> url = http://101.132.73.130:6800/
> project = ProjectName
> username = ServerUserName
> password = ServerPassWord
>
> [deploy:DeloyName]
> url = http://39.108.175.25:6800/
> project = ProjectName
> username = ServerUserName
> password = ServerPassWord
> ```

​	说明：

​	deploy：scrapyd部署的时候的名称；

​	url：服务器地址

​	project：项目名称

​	username：服务器帐号名

​	password：服务器密码

​	其中每个deploy的名字不能相同，不同服务器的project最好相同，方便后续操作。请根据实际情况配置。



#### 配置settings

​	settings文件中的Redis数据库和MySQL数据库的配置需要根据自己实际情况配置。

​	另外请把middlewares的代理池注释掉，或者将utils文件夹中的config_MySQL.py修改指向自己的代理池。



#### Scrapyd部署

​	进入与scrapy.cfg文件同级目录下：

​	1.开启scrapyd服务：在shell运行命令`scrapyd`即可

​	2.开启另外一个shell，进入到和scrapy.cfg文件同级目录，运行以下命令：`scrapyd-deploy localspider -p LagouRedis`，接收到成功消息即成功将项目部署到scrapyd服务。

​	3.重复2命令在不同服务器上配置项目。



#### 启动项目运行

​	1.在scrapy.cfg文件同级目录下，在shell运行命令：

​	`python scrapyd_run.py -h`

​	可以查看其使用方法。使用前请先进入scrapyd_run.py文件配置好说明里面的需要配置的信息。

​	2.运行`python scrapyd_run.py -S`可以运行刚才部署的爬虫项目。

​	3.运行`python scrapyd_run.py -s`可以查看对应服务器的scrpayd服务的运行状态

​	4.运行`python scrapyd_run.py -lj`可以查看对应服务器对应项目的jobid

​	5.运行`python scrapyd_run.py -C jobid`可以取消运行的爬虫项目(可能需要执行两次，第二次爬虫任务确认停止)，jobid是4命令中得到，也可以在浏览器打开scrapyd服务地址得到。

​	6.有多个服务器是可以加上`-a num`参数来指定对应的服务器。

​	7.更多命令请`python scrapyd_run.py -h`来获得帮助



## Bug

​	如遇Bug请邮件我(1306513796@qq.com), 或者有任何改进意见也可邮件我~

​	已知缺陷：

​		1.IP代理数量不足以高速爬取拉勾网，我是自建IP代理池，池中经过检测也就60余个可用IP(用百度作检测的)。所以土豪们可以购买代理并修改settings.py中对速度限制，提高爬取速度。

​		2.Cookies没有进行实时更新，爬取两三天后被拉勾网站拒绝次数增多，数据爬取速度也会down下来...当然用大量代理IP是可以不用cookies。



## 说明

​	仅作学习交流使用！





