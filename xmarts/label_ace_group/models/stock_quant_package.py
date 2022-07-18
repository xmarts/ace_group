from odoo import models, fields, api

class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'

    receipe_number = fields.Char(
            string='Receipt Number', 
    )
    receipe_id = fields.Many2one(
        'stock.picking', 
        string='Receipt', 
        compute="_compute_receipe", 
        search="_search_receipe",
        store=False)

    @api.depends("picking_ids")
    def _compute_receipe(self):
        for rec in self:    
            rec.receipe__id = False
            picking_id = self.env['stock.picking'].search([('id','in',rec.picking_ids.ids),('picking_type_id','=','incoming')], limit=1)
            if picking_id:
                rec.receipe_id = picking_id.id

    def _search_receipe(self, operator, value):
        domain = [('picking_id', operator, value)]
        data = self.env['stock.package_level'].sudo().search(domain)
        return [('id', 'in', data.mapped('package_id.id'))]        

class StockPackageLevel(models.Model):
    _inherit = 'stock.package_level'
    _order = 'location_dest_name, id'

    location_dest_name = fields.Char('Location Dest. Name', related="location_dest_id.name", store=True)