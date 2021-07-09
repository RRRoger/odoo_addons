# -*- coding: utf-8 -*-
from odoo import http

# class IrActionsEnhance(http.Controller):
#     @http.route('/ir_actions_enhance/ir_actions_enhance/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ir_actions_enhance/ir_actions_enhance/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('ir_actions_enhance.listing', {
#             'root': '/ir_actions_enhance/ir_actions_enhance',
#             'objects': http.request.env['ir_actions_enhance.ir_actions_enhance'].search([]),
#         })

#     @http.route('/ir_actions_enhance/ir_actions_enhance/objects/<model("ir_actions_enhance.ir_actions_enhance"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ir_actions_enhance.object', {
#             'object': obj
#         })