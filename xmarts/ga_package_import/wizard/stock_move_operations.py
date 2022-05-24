# -*- coding: utf-8 -*-

from odoo import api, fields, models


class StockMoveOperation(models.TransientModel):
    _name = "wiz.stock.move"
    _description = "Select Package"
    
    @api.model
    def _get_package_id(self):
        packages = []
        if self._context.get('active_id'):
            stock = self.env['stock.move'].browse(self._context.get('active_id'))
            packages = stock.product_id.packaging_ids.ids
        self.package_id = packages and packages[0] or False    
        return {'domain': {'package_id': [('prduct_id', 'in', packages)]}}

    package_id = fields.Many2one('product.packaging', string='Package', required=True, default=_get_package_id)
