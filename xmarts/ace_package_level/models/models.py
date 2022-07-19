# from odoo import models, fields, api


# class /odoo/henca/henca_account_report(models.Model):
#     _name = '/odoo/henca/henca_account_report./odoo/henca/henca_account_report'
#     _description = '/odoo/henca/henca_account_report./odoo/henca/henca_account_report'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
