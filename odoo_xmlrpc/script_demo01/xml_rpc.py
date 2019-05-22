# -*- encoding: utf-8 -*-

import string, os, sys, xmlrpclib, datetime, json, xlrd, re, ssl ,requests, ConfigParser
# import 上级目录
sys.path.append("..")

from sockObj import get_sock, DB, USERPASS
sock, uid = get_sock()


# 业务代码 Start ...

print sock.execute(DB, uid, USERPASS, 'res.partner', 'search', [('id', '<', 20)])  # 返回确认





