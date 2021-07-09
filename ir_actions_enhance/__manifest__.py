# -*- coding: utf-8 -*-
{
    'name': "ir_actions_enhance",

    'summary': """
        ir_actions_enhance
    """,

    'description': """
        1. model `ir.actions.server` add json_dumps function
    """,

    'author': "Roger",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/10.0/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}