# -*- coding: utf-8 -*-
# from odoo import http


# class Marbleshope(http.Controller):
#     @http.route('/marbleshope/marbleshope/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/marbleshope/marbleshope/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('marbleshope.listing', {
#             'root': '/marbleshope/marbleshope',
#             'objects': http.request.env['marbleshope.marbleshope'].search([]),
#         })

#     @http.route('/marbleshope/marbleshope/objects/<model("marbleshope.marbleshope"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('marbleshope.object', {
#             'object': obj
#         })
