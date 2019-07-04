# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': '数据库操作',
    'summary': '数据库操作',
    'sequence': '19',
    'category': 'Project',
    'depends': [],
    'description': """
DB STATEMENT

本模块专用于管理员操作数据库,
可用于临时查询数据 & 紧急修复数据库.
        """,
    'data': [
        'send_mail_wizard.xml',
        'db_statement.xml',
        'security/ir.model.access.csv',
    ],
    'application': True,
}
