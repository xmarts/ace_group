# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import time
from ast import literal_eval
from collections import defaultdict
from datetime import date
from itertools import groupby
from operator import attrgetter, itemgetter

from odoo import SUPERUSER_ID, _, api, fields, models
from odoo.addons.stock.models.stock_move import PROCUREMENT_PRIORITIES
from odoo.exceptions import UserError
from odoo.osv import expression
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, format_datetime
from odoo.tools.float_utils import float_compare, float_is_zero, float_round
from odoo.tools.misc import format_date

import logging

_logger = logging.getLogger(__name__)

class StockMove(models.Model):
    _inherit = "stock.move"

    def _search_picking_for_assignation(self):
        if 'siempre_origen' in self._context:
            self.ensure_one()
            picking = self.env['stock.picking'].search([
                    ('group_id', '=', self.group_id.id),
                    ('location_id', '=', self.location_id.id),
                    ('location_dest_id', '=', self.location_dest_id.id),
                    ('picking_type_id', '=', self.picking_type_id.id),
                    ('origin', '=', self._context.get('siempre_origen')),
                    ('printed', '=', False),
                    ('immediate_transfer', '=', False),
                    ('state', 'in', ['draft', 'confirmed', 'waiting', 'partially_available', 'assigned'])], limit=1)
            return picking     
        return super(StockMove, self)._search_picking_for_assignation()

class Picking(models.Model):
    _inherit = "stock.picking"

    def _autoconfirm_picking(self):        
        return super(Picking, self.with_context(siempre_origen=self.name))._autoconfirm_picking()
   
