# -*- encoding: utf-8 -*-

import string, os, sys, xmlrpclib, datetime, json, xlrd, re, ssl ,requests, ConfigParser
# import 上级目录
sys.path.append("..")

from sockObj import get_sock, DB, USERPASS
from log import _log, SUCCESS, WARNING, ERROR
sock, uid = get_sock()


# 业务代码 Start ...


# log 用法
_log("I AM A LOG...", SUCCESS)

# xmlrpc 调用方式
print sock.execute(DB, uid, USERPASS, 'res.partner', 'search', [('id', '<', 20)])  # 返回确认





