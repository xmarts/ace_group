# -*- coding: utf-8 -*-
{
    'name': "Package Import",

    'summary': """
        Package Import form other picking""",

    'description': """
        Package Import form other picking
    """,

    'author': "DSA SOftware SG, C.A.",
    'website': "http://www.dsasoftware.com.ve",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock',                
                ],

    # always loaded
    'data': [                        
        'views/stock_picking_views.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
}
