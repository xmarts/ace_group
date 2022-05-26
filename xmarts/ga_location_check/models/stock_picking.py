# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

import logging

_logger = logging.getLogger(__name__)


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    def button_validate(self):
        for rec in self:
            location = False
            if rec.picking_type_id.code=='internal' and rec.location_dest_id.ga_is_check_package_done:
                location = rec.location_dest_id
            if rec.picking_type_id.code=='incoming' and rec.location_dest_id.ga_is_check_package_done:
                location = rec.location_dest_id
            if rec.picking_type_id.code=='outgoing' and rec.location_id.ga_is_check_package_done:
                location = rec.location_id
            _logger.info("location: %s"%location)
            if location and rec.package_level_ids_details:
                for x in rec.package_level_ids_details:
                    _logger.info("X: %s"%x)
                    if not x.is_done:
                        raise ValidationError("Error. Este almacen esta restringido a no procesar packages done")
                        return False        
        return super(StockPicking, self).button_validate()