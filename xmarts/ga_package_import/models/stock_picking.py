# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'
       
    def action_put_in_pack2(self, picking_id, location_id, location_dest_id):
        self.ensure_one()
        _logger.info(' ********************* TEST: *******************')
        #picking_id = self.env.context.get("import_picking_id")
        #picking_id = self.env['stock.picking'].browse()
        if picking_id:
            if picking_id.owner_id:
                self.owner_id = picking_id.owner_id.id
            for package in picking_id.package_level_ids:
                self.env['stock.package_level'].create(
                                                    {'package_id':package.package_id.id,
                                                     'picking_id': self.id, 
                                                     'location_id': location_id.id,
                                                     'location_dest_id': location_dest_id.id,
                                                     'company_id': self.company_id.id})

            
