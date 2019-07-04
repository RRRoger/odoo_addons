# -*- encoding: utf-8 -*-

import string
import os
import sys
import xmlrpclib
import datetime
import json
import xlrd
import re
import ssl
import requests
import ConfigParser

# import 上级目录
sys.path.append("..")
from log import SUCCESS, ERROR, WARNING, _log

reload(sys)
sys.setdefaultencoding('utf-8')
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

PATH = "../rpc.conf"
cf = ConfigParser.ConfigParser()
cf.read(PATH)

env = dict(cf.items('ENV'))
env_name = env['env_name']
confs = dict(cf.items(env_name))

_log('ENV: %s' % (env_name, ), SUCCESS)

for i in ['username', 'db', 'host', 'https', 'userpass', 'port']:
    k, v = i.upper(), confs.get(i)
    _log('%s:%s' % (k, '******' if k == 'USERPASS' else v), SUCCESS)
    exec "%s = confs.get('%s')" % (i.upper(), i)

def get_sock():
    if HTTPS=='1':
        sock_common = xmlrpclib.ServerProxy ('https://%s/xmlrpc/common' % (HOST,), verbose=False, use_datetime=True, context=ssl_ctx)
        uid = sock_common.login(DB, USERNAME, USERPASS)
        sock = xmlrpclib.ServerProxy('https://%s/xmlrpc/object' % (HOST,), verbose=False, use_datetime=True, context=ssl_ctx)
    else:
        sock_common = xmlrpclib.ServerProxy ('http://%s:%s/xmlrpc/common' % (HOST,PORT))
        uid = sock_common.login(DB, USERNAME, USERPASS)
        sock = xmlrpclib.ServerProxy('http://%s:%s/xmlrpc/object' % (HOST,PORT))
    return sock, uid
