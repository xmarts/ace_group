# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)

class StockPicking(models.Model):
    _inherit = 'stock.picking'
       
    ga_po_number = fields.Char("PO NUmber")
    ga_inventory_type = fields.Char("Inventory Type")
    ga_weight = fields.Char("Weight")
    ga_seal_number = fields.Char("Seal Number")
    ga_truck_number = fields.Char("Truck Number")
    ga_container_number = fields.Char("Container Number")
    ga_weight = fields.Char("Weight")
    ga_truck_license = fields.Char("Truck License")
    ga_trailer_license = fields.Char("Trailer License")
