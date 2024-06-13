# -*- coding: utf-8 -*-
# from odoo import http


# class Talebehane(http.Controller):
#     @http.route('/talebehane/talebehane', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/talebehane/talebehane/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('talebehane.listing', {
#             'root': '/talebehane/talebehane',
#             'objects': http.request.env['talebehane.talebehane'].search([]),
#         })

#     @http.route('/talebehane/talebehane/objects/<model("talebehane.talebehane"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('talebehane.object', {
#             'object': obj
#         })
