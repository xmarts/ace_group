# -*- coding: utf-8 -*-
{
    'name': "Location Check",

    'summary': """
        Validate packages not state done""",

    'description': """
        Validate packages not state done
    """,

    'author': "DSA SOftware SG, C.A.",
    'website': "http://www.dsasoftware.com.ve",

    'category': 'Warehouse',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['stock',                
                ],

    # always loaded
    'data': [                        
        'views/stock_location_view.xml',              
    ],
    # only loaded in demonstration mode
    'demo': [],
}
