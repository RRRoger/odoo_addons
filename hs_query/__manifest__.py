# -*- coding: utf-8 -*-

{
    'name': 'HS-Tech Query',
    'version': '1.3',
    'category': 'Query',
    'sequence': 15,
    'author': 'Roger',
    'summary': 'HS-Tech Query',
    'description': """
    """,
    'website': '',
    'depends': ['base'],
    'data': [
        'security/group_security.xml',

        'views/templates.xml',
        'views/web_action.xml',
        'views/query.xml',
        'views/query_select_wizard_parent.xml',
        'views/query_input_cache.xml',

        'query_demo/query_demo_report.xml',
        'query_demo/query_demo_data.xml',

        'views/menu.xml',

        'data/data.xml',

        # 'data/data.xml',
        'security/ir.model.access.csv',
    ],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
