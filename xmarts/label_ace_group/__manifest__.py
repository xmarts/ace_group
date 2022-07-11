# -*- coding: utf-8 -*-
{
    'name': "Picking Label Custom (Ace Group)",

    'summary': """
        Picking Label Custom (Ace Group)""",

    'description': """
        Picking Label Custom (Ace Group)
    """,

    'author': "DSA Software SG, C.A:",
    'website': "http://www.dsasoftware.com.ve",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Warehouse',
    'version': '0.0.0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock','ga_stock_prearrival'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        #'data/data.xml',
        #'views/views.xml',
        'views/stock_quant_package_view.xml',
        'report/stock_report_views.xml',
        'report/report_package_barcode_ace.xml',
        'report/report_package_zpl.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
