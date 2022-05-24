# -*- coding: utf-8 -*-

from odoo import api, fields, models

import logging

_logger = logging.getLogger(__name__)


class StockMoveOperation(models.TransientModel):
    _name = "wiz.button.move.package"
    _description = "Select Location"
            
    location_dest_id = fields.Many2one('stock.location', string='Destination Location', required=True)

    def approve_activity(self):
        _logger.info('****CONTEXT****:%s'%self._context)
        if 'default_move_line_id' in self._context:
            move_line = self.env['stock.move.line'].browse(self._context.get('default_move_line_id'))
            if move_line.result_package_id:
                move_line.result_package_id.write({'location_id':self.location_dest_id.id})            
            move_line.write({'location_dest_id':self.location_dest_id.id})
        else:
            if self._context.get('active_ids'):
                for package in self.env['stock.quant.package'].browse(self._context.get('active_ids')):
                    package.move_package(self.location_dest_id)
            elif self._context.get('active_id'):
                for package in self.env['stock.quant.package'].browse(self._context.get('active_id')):
                    package.move_package(self.location_dest_id)                          
        return True