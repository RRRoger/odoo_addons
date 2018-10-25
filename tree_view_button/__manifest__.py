# -*- coding: utf-8 -*-

{
    'name': 'Tree View Button',
    'version': '1.0.2',
    'category': 'Tools',
    'sequence': 12,
    'author': 'Roger',
    'summary': 'Tree View Button',
    'description': """
==================================

Tree View Button

----------------------------------
    """,
    'website': '',
    'depends': ['base'],
    'data': [
        'views/tree_button.xml',
    ],
    'qweb': [
        'static/src/xml/qweb_tree_button.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
