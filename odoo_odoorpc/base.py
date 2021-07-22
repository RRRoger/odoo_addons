# -*- encoding: utf-8 -*-

import os, sys
import datetime, time
import ConfigParser
import odoorpc

reload(sys)
sys.setdefaultencoding('utf-8')

SUCCESS, ERROR, WARNING = 'SUCCESS', 'ERROR', 'WARNING'


def _log(info, level=SUCCESS):
    print(info)
    with open('log.log', 'a+') as f:
        f.write('%s %s %s\n' % (level, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"), info))


PATH = "./rpc.conf"
cf = ConfigParser.ConfigParser()
cf.read(PATH)

env = dict(cf.items('ENV'))
env_name = env['env_name']
confs = dict(cf.items(env_name))

HTTPS, HOST, PORT, DB, USERNAME, USERPASS = '', '', 80, '', '', ''

for i in ['username', 'db', 'host', 'https', 'userpass', 'port']:
    k, v = i.upper(), confs.get(i)
    _log('%s:%s' % (k, '******' if k == 'USERPASS' else v), SUCCESS)
    exec "%s = confs.get('%s')" % (i.upper(), i)

if HTTPS == '1':
    odoo = odoorpc.ODOO(HOST, protocol="jsonrpc+ssl", port=PORT)
else:
    odoo = odoorpc.ODOO(HOST, port=PORT)

odoo.login(DB, USERNAME, USERPASS)

Partner = odoo.env['res.partner']
partner_ids = Partner.search([('id', '>', 0), ('id', '<', 20)])
for partner_id in partner_ids:
    partner = Partner.browse(partner_id)
    print(partner.name)
