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
            if rec.picking_type_id=='internal' and rec.location_dest_id.ga_is_check_package_done:
                location = rec.location_dest_id
            if rec.picking_type_id=='incoming' and rec.location_dest_id.ga_is_check_package_done:
                location = rec.location_dest_id
            if rec.picking_type_id=='outgoing' and rec.location_id.ga_is_check_package_done:
                location = rec.location_id
            if location and rec.packages_level_ids_details:
                if any(x.is_done for x in rec.packages_level_ids_details):
                    raise ValidationError("Error. Este almacen esta restringido a no procesar packages done")
                    return False        
        return super(StockPicking, self).button_validate()

    @api.constrains("state")
    def check_package_done(self):
        for rec in self:
            location = False
            if rec.picking_type_id=='internal' and rec.location_dest_id.ga_is_check_package_done:
                location = rec.location_dest_id
            if rec.picking_type_id=='incoming' and rec.location_dest_id.ga_is_check_package_done:
                location = rec.location_dest_id
            if rec.picking_type_id=='outgoing' and rec.location_id.ga_is_check_package_done:
                location = rec.location_id
            if location and rec.packages_level_ids_details:
                if any(x.is_done for x in rec.packages_level_ids_details):
                    raise ValidationError("Error. Este almacen esta restringido a no procesar packages done")
                    return False
