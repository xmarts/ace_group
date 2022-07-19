from odoo import models, fields, api

class StockPackageLevel(models.Model):
    _inherit = 'stock.package_level'

    product_id = fields.Many2one('product.product', compute='_compute_extras')
    product_qty = fields.Float('Location Dest. Name', compute='_compute_extras')
    picking_incoming_id = fields.Many2one('stock.picking', compute='_compute_extras')

    @api.depends("package_id","package_id.quant_ids")
    def _compute_extras(self):
        for rec in self:    
            rec.product_id = False
            rec.product_qty = 0
            rec.picking_incoming_id = False
            pack_level = self.env['stock.move.line'].search([('package_level_id','=',rec.id)], limit=1)
            if pack_level:
                rec.product_id = pack_level.product_id.id
                rec.product_qty = pack_level.qty_done            
            domain = ['|', ('result_package_id', '=', rec.package_id.id), ('package_id', '=', rec.package_id.id)]
            pickings = self.env['stock.move.line'].search(domain)
            if pickings:                
                for move in pickings:
                    if move.picking_code=='incoming':
                        rec.picking_incoming_id = move.picking_id.id

    @api.model
    def _compute_operation_valid(self):
        res = True
        for move in self.move_line_ids:
            res &= move._compute_operation_valid()
        return res                           
