# -*- coding: utf8 -*-
from fabric.api import *
from fabric.contrib.console import confirm

node1 = 'user@addr'
node2 = 'user@addr'
node3 = 'user@addr'

env.roledefs = {
    'scheduler': [node3],
    'crawler': [node1, node2],
    'nodes': [node1, node2, node3]
}


# 初始化环境
@roles('nodes')
@parallel
def setup_common():
    run('yum -y update')
    run('yum install -y glibc-devel glibc-headers python-devel python-pip libzip-devel readline-devel zlib-devel bzip2-devel python-setuptools patch libxslt-devel libxml2')
    run('yum install -y redis erlang')


# 可以参照 https://www.rabbitmq.com/install-rpm.html
# 然后手动安装
# rabbitmq guest 默认只有 localhost 的访问权限, 需要设置一下 https://www.rabbitmq.com/access-control.html
# yum install -y mongodb mongodb-server 安装 MongoDB
@roles('scheduler')
def setup_rabbitmq():
    pass


@roles('nodes')
@parallel
def first_deploy():
    try:
        run('mkdir /app')
    except:
        pass

    run('cd /app && git clone https://github.com/caitong93/bishe.git')
    run('cd /app/bishe && pip install -r requirements.txt')


@roles('nodes')
@parallel
def re_deploy():
    try:
        run('mkdir /app')
    except:
        pass
    try:
        run('rm -r -f /app/bishe')
    except:
        pass
    run('cd /app && git clone https://github.com/caitong93/bishe.git')
    run('cd /app/bishe && pip install -r requirements.txt')


@roles('nodes')
@parallel
def deploy():
    run('cd /app/bishe && git pull')
    run('cd /app/bishe && pip install -r requirements.txt')

####### Startup

# 需要先启动 redis-server 和 rabbitmq-server
@roles('scheduler')
def start_scheduler():
    run('cd /app/bishe/letscrawl/letscrawl && sh scheduler_startup.sh')


# 需要先启动 redis-server
@roles('crawler')
@parallel
def start_crawler():
    run('cd /app/bishe/letscrawl/letscrawl && sh crawler_startup.sh')

########## Demos

@roles('crawler')
@parallel
def uname():
    run('uname -a')


@hosts('a', 'b')
@roles('role1')
def mytask():
    run('ls /var/www')