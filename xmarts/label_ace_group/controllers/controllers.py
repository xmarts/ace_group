# -*- coding: utf-8 -*-
# from odoo import http


# class /odoo/henca/hencaAccountReport(http.Controller):
#     @http.route('//odoo/henca/henca_account_report//odoo/henca/henca_account_report/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//odoo/henca/henca_account_report//odoo/henca/henca_account_report/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('/odoo/henca/henca_account_report.listing', {
#             'root': '//odoo/henca/henca_account_report//odoo/henca/henca_account_report',
#             'objects': http.request.env['/odoo/henca/henca_account_report./odoo/henca/henca_account_report'].search([]),
#         })

#     @http.route('//odoo/henca/henca_account_report//odoo/henca/henca_account_report/objects/<model("/odoo/henca/henca_account_report./odoo/henca/henca_account_report"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/odoo/henca/henca_account_report.object', {
#             'object': obj
#         })
