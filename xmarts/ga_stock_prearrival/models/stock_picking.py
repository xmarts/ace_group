# -*- coding: utf-8 -*- 

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)

class StockPickingType(models.Model):
    _inherit = 'stock.picking.type'

    count_picking_prearrival = fields.Integer(compute='_compute_picking_prearrival_count')            
            
    def _compute_picking_prearrival_count(self):
        domains = {
            'count_picking_prearrival': [('state', '=', 'prearrival')],
        }
        for field in domains:
            data = self.env['stock.picking'].read_group(domains[field] +
                [('state', 'not in', ('done', 'cancel')), ('picking_type_id', 'in', self.ids)],
                ['picking_type_id'], ['picking_type_id'])
            count = {
                x['picking_type_id'][0]: x['picking_type_id_count']
                for x in data if x['picking_type_id']
            }
            for record in self:
                record[field] = count.get(record.id, 0)                

    def get_action_picking_tree_prearrival(self):
        return self._get_action('ga_stock_prearrival.action_picking_tree_arrival')

class StockPicking(models.Model):
    _inherit = 'stock.picking'

    partner_id = fields.Many2one('res.partner', string="Shipper")
    # state = fields.Selection(selection_add=[])
    state = fields.Selection([
        ('draft', 'Draft'),
        ('waiting', 'Waiting Another Operation'),
        ('confirmed', 'Waiting'),
        ('prearrival','Pre-Arrival'),
        ('assigned', 'Ready'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], string='Status', compute='_compute_state',
        copy=False, index=True, readonly=True, store=True, tracking=True,
        help=" * Draft: The transfer is not confirmed yet. Reservation doesn't apply.\n"
             " * Waiting another operation: This transfer is waiting for another operation before being ready.\n"
             " * Waiting: The transfer is waiting for the availability of some products.\n(a) The shipping policy is \"As soon as possible\": no product could be reserved.\n(b) The shipping policy is \"When all products are ready\": not all the products could be reserved.\n"
             " * Ready: The transfer is ready to be processed.\n(a) The shipping policy is \"As soon as possible\": at least one product has been reserved.\n(b) The shipping policy is \"When all products are ready\": all product have been reserved.\n"
             " * Done: The transfer has been processed.\n"
             " * Cancelled: The transfer has been cancelled.")
    
    consigne = fields.Char('Consigne', size=40)
    bol = fields.Char('Bol', size=40)
    whse = fields.Many2one('stock.prearrival.whse',string='Whse')
    
    
    def button_prearrival(self):
        if self.state=='draft':
            self.write({'state': 'prearrival'})
            
    
    def button_arrival_done(self):
        if self.state=='prearrival':
            return self.action_confirm()    
    
    def action_put_in_pack(self):
        self.ensure_one()
        """
        picking_move_lines = self.move_line_ids
        if not self.picking_type_id.show_reserved:
            picking_move_lines = self.move_line_nosuggest_ids  
        move_line_ids = picking_move_lines.filtered(lambda ml:
            float_compare(ml.qty_done, 0.0, precision_rounding=ml.product_uom_id.rounding) > 0
            and not ml.result_package_id
        )
        """  
        _logger.info(' ********************* TEST: *******************')
        move_line_ids = False

        """
        for move in move_line_ids:
            if move.product_id.packaging_ids:
                packaging_id = move.product_id.packaging_ids[0]
                if packaging_id.qty>0:
                    qty_aviable = move.product_uom_qty - move.quantity_done 
                    nitems = qty_aviable/packaging_id.qty
                    nmas = (1 if nitems-int(nitems)>0 else 0)
                    nitems = int(nitems)+nmas
                    for rec in range(0,nitems):                                        
                        if not move.qty_done:
                            if move.product_uom_qty>packaging_id.qty:
                                qty = packaging_id.qty
                            else:
                                qty = move.product_uom_qty
                            move.write({'qty_done':qty})
                            move_line_ids_2 = move.picking_id.move_line_ids.filtered(lambda o: o.qty_done > 0 and not o.result_package_id)
                            if move_line_ids_2:
                                move.picking_id._put_in_pack(move_line_ids_2)
                                """        
                                
        for record in self.move_ids_without_package:
            _logger.info('Test 1: %s'%record)
            if record.product_id.packaging_ids:
                packaging_id = record.product_id.packaging_ids[0]
                if packaging_id.qty>0:
                    qty_aviable = record.product_uom_qty - record.quantity_done 
                    nitems = qty_aviable/packaging_id.qty
                    nmas = (1 if nitems-int(nitems)>0 else 0)
                    nitems = int(nitems)+nmas
                    for rec in range(0,nitems):                    
                        for move in record.move_line_ids:
                            if not move.qty_done:
                                if move.product_uom_qty>packaging_id.qty:
                                    qty = packaging_id.qty
                                else:
                                    qty = move.product_uom_qty
                                move.write({'qty_done':qty})
                                move_line_ids = move.picking_id.move_line_ids.filtered(lambda o: o.qty_done > 0 and not o.result_package_id)
                                if move_line_ids:
                                    res = self._pre_put_in_pack_hook(move_line_ids)
                                    if not res:
                                        res = self._put_in_pack(move_line_ids)                                    
                                    #move.picking_id._put_in_pack(move_line_ids)
      
        if move_line_ids:
            return True
                                     
        return super(StockPicking,self).action_put_in_pack()            
        
class StockMove(models.Model):
    _inherit = 'stock.move'
    
    
    def button_auto_package(self):
        for record in self:
            if record.product_id.packaging_ids:
                for x in record:
                    _logger.info('record x:%s'%x)
                _logger.info('packaging_ids:%s'%record.product_id.packaging_ids)
                packaging_id = record.product_id.packaging_ids[0]
                _logger.info('packaging_id:%s'%packaging_id)
                _logger.info('qty x pack:%s'%packaging_id.qty)
                if packaging_id.qty>0:
                    qty_aviable = self.product_uom_qty - self.quantity_done 
                    nitems = qty_aviable/packaging_id.qty
                    nmas = (1 if nitems-int(nitems)>0 else 0)
                    nitems = int(nitems)+nmas
                    _logger.info('product_uom_qty:%s'%qty_aviable)
                    _logger.info('nitems:%s'%nitems)
                    for rec in range(0,nitems):                    
                        for move in record.move_line_ids:
                            if not move.qty_done:
                                if move.product_uom_qty>packaging_id.qty:
                                    qty = packaging_id.qty
                                else:
                                    qty = move.product_uom_qty
                                move.write({'qty_done':qty})
                                move_line_ids = move.filtered(lambda ml: float_compare(ml.product_uom_qty, 0.0,
                                                     precision_rounding=ml.product_uom_id.rounding) > 0 and float_compare(ml.qty_done, 0.0,
                                                     precision_rounding=ml.product_uom_id.rounding) == 0)
                                if move_line_ids:                                 
                                    move.picking_id._put_in_pack(move_line_ids)                                            
        return True
        
class StockQuantPackage(models.Model):
    _inherit = 'stock.quant.package'
                  
    picking_ids = fields.Many2many('stock.picking', string='Transfers List', compute="get_picking_transfer", store=True)
    picking_referens = fields.Char(string='Referencs Transfers List', compute="get_picking_transfer", store=True)
    current_picking_id = fields.Many2one('stock.picking', string='Transfer', compute="get_picking_transfer", store=True)
    current_reference = fields.Char(string='Reference', compute="get_picking_transfer", store=True)
    
    @api.depends('location_id')
    def get_picking_transfer(self):
        for record in self:
            domain = ['|', ('result_package_id', '=', record.id), ('package_id', '=', record.id)]
            #pickings = self.env['stock.move.line'].search(domain).mapped('picking_id')
            sml_obj = self.env['stock.move.line'].search(domain)
            pickings_list = []
            referens_list = ""
            reference = ""
            picking_id = False            
            for move in sml_obj:
                #if move.location_dest_id.id==record.location_id.id:
                picking_id = move.picking_id.id
                reference = move.reference or "" 
                pickings_list.append(picking_id)
                if reference:
                    if referens_list:
                        referens_list += ','                
                    referens_list += reference
            record.picking_ids = self.env['stock.picking'].search([('id','in',pickings_list)]).ids
            record.picking_referens = referens_list    
            record.current_picking_id = picking_id
            record.current_reference = reference
            
    def _search_owner(self, operator, value):
        if value:
            packs = self.search([('current_picking_id', operator, value)])
            if packs:
                return [('id', 'parent_of', packs.ids)]        
        return super(StockQuantPackage,self)._search_owner(operator, value)                  
    
    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = list(args or [])
        args += [('current_reference', operator, name)]
        return super(StockQuantPackage,self).name_search(name, args, operator, limit)                      
                         
    def move_package(self, destination):
        imediate_obj=self.env['stock.immediate.transfer']
        copy_record = self.env['stock.picking'] # now you call the method directly
        for record in self:
            _logger.info('record:%s'%record)
            if destination and destination.id!=record.location_id.id:
                _logger.info('destination:%s'%destination)
                move_line = self.env['stock.move.line'].search([('result_package_id','=',record.id)])
                _logger.info('move_line:%s'%move_line)
                pikcing = False                
                for move in move_line:                    
                    pikcing = move.picking_id
                    qty = move.qty_done
                    _logger.info('pikcing 0:%s'%pikcing)
                if pikcing:
                    _logger.info('pikcing 1:%s'%pikcing)
                    pikcing = copy_record.browse(pikcing.id).copy()
                    for line in pikcing.move_ids_without_package:
                        line.product_uom_qty = qty
                    data_pk = {'location_id':record.location_id.id,
                               'location_dest_id':destination.id,
                               'scheduled_date':fields.Date.today(),
                               'date_done':False}
                    pikcing.write({'location_id':record.location_id.id,'location_dest_id':destination.id})
                    _logger.info('pikcing 2:%s'%pikcing)  
                    pikcing.action_confirm()
                    pikcing.action_assign()
                    imediate_rec = imediate_obj.create({'pick_ids': [(4, pikcing.id)]})
                    imediate_rec.process()                    
                    move_line = self.env['stock.move.line'].search([('picking_id','=',pikcing.id)])
                    for line in move_line:
                        line.write({'package_id':record.id,'result_package_id':record.id})
                    if pikcing.state !='done':
                        for move in pikcing.move_ids_without_package:
                            move.quantity_done = move.product_uom_qty
                        pikcing.button_validate()                        
            record._cr.commit()                 

        return True
                                        
            
class StockPrearrivalWhse(models.Model):
    _name = 'stock.prearrival.whse'
    _descripcions = 'stock.prearrival.whse'
    
    name = fields.Char('Name', size=40, required=True)
    
class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'    
    
    def action_assign_destination_location(self):
        """ Opens a wizard to assign SN's name on each move lines.
        """
        self.ensure_one()
        
        #action = self.env.ref('stock.act_assign_serial_numbers').read()[0]
        action = self.env.ref('ga_stock_prearrival.action_wiz_button_move_package').read()[0]
        action['context'] = {
            'default_picking_id': self.picking_id.id,
            'default_move_line_id': self.id,
            'default_move_id': self.move_id.id,
            'default_package_id': self.package_id.id,
        }
        return action       