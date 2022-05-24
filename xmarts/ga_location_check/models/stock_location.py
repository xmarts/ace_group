# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)


class StockLocation(models.Model):
    _inherit = 'stock.location'
       
    ga_is_check_package_done = fields.Boolean('Check Packages not done', default=False)
            
