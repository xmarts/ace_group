# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

{
    'name': 'Ventor Base',
    'version': '14.0.1.4.0',
    'author': 'VentorTech',
    'website': 'https://ventor.tech/',
    'license': 'LGPL-3',
    'installable': True,
    'images': ['static/description/main_banner.png'],
    'summary': 'Base module that allow relation between Ventor modules',
    'depends': [
        'base',
        'stock',
        'stock_picking_batch',
    ],
    'data': [
        'security/groups.xml',
        "data/00_ir_action_server_data.xml",
        'views/res_config.xml',
        'views/res_users.xml',
        'views/stock_inventory.xml',
        'views/stock_location.xml',
        'views/stock_picking.xml',
        'views/stock_warehouse.xml',
    ],
    'post_init_hook': '_post_init_hook',
}
