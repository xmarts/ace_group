# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class StockMoveOperation(models.TransientModel):
    _name = "wiz.import.package"
    _description = "Package Import"
            
    import_picking_id = fields.Many2one('stock.picking', string='Document Number', required=True)

    def action_importar(self):
        _logger.info('active_ids: %s'%self.env.context['active_ids'])
        for picking in self.env['stock.picking'].browse(self.env.context['active_ids']):
            _logger.info('picking: %s'%self.env.context['active_ids'])
            picking.action_put_in_pack2(self.import_picking_id, picking.location_id, picking.location_dest_id)

