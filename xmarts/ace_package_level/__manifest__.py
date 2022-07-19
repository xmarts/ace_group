# -*- coding: utf-8 -*-
{
    'name': "Package Level Custom (Ace Group)",

    'summary': """
        Package Level Custom (Ace Group)""",

    'description': """
        Package Level Custom (Ace Group)
    """,

    'author': "DSA Software SG, C.A:",
    'website': "http://www.dsasoftware.com.ve",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock'],

    # always loaded
    'data': [
        'views/package_level_view.xml',
        'views/templates.xml',
    ],
}
