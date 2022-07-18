# Copyright 2020 VentorTech OU
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl-3.0).

from . import models
from odoo import api, SUPERUSER_ID

def _post_init_hook(cr, registry):
    """
    This hook updates Ventor Settings in Operation Types
    And adds to all users to Ventor - Administrator Role
    """
    env = api.Environment(cr, SUPERUSER_ID, {})

    all_stock_inventory_ids = env["stock.inventory"].search(
        [
            ("location_ids", "!=", False),
        ]
    )
    for stock_inv in all_stock_inventory_ids:
        warehouse_ids = stock_inv.location_ids.mapped("warehouse_id")
        if len(warehouse_ids) == 1:
            stock_inv.warehouse_id = warehouse_ids

    users_model = env['res.users']

    values = [(4, user.id) for user in users_model.search([])]
    env.ref('ventor_base.ventor_role_admin').users = values

    cr.execute(
        """
        UPDATE stock_picking_type
        SET
            change_destination_location = True,
            show_next_product = CASE code when 'incoming' THEN False ELSE True END
        """
    )

    users = users_model.with_context(active_test=False).search([
            ('allowed_warehouse_ids', '=', False),
            ('share', '=', False)
            ])
    warehouses = env["stock.warehouse"].with_context(active_test=False).search([])
    for user in users:
        user.allowed_warehouse_ids = [(6, 0, warehouses.ids)]

    # Update warehouse_id for all locations
    all_locations = env['stock.location'].with_context(active_test=False).search([
            ('warehouse_id', '=', False),
            ])
    all_locations.action_update_warehouse()
