# -*- coding: utf-8 -*-
{
    'name': "Stock Prearrival",

    'summary': """
        Stock prearrival""",

    'description': """
        Stock prearrival
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
        'wizard/stock_transfer_view.xml',        
        'views/stock_picking_views.xml',
        'views/stock_move_line_views.xml',
        'views/stock_quant_package_views.xml',
        'report/report_package_barcode_ace.xml',
        'report/stock_report_views.xml',
        'security/ir.model.access.csv',
        'data/data.xml',
        # 'data/img/logo.jpg',        
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
