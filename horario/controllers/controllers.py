# -*- coding: utf-8 -*-
# from odoo import http


# class Horario(http.Controller):
#     @http.route('/horario/horario/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/horario/horario/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('horario.listing', {
#             'root': '/horario/horario',
#             'objects': http.request.env['horario.horario'].search([]),
#         })

#     @http.route('/horario/horario/objects/<model("horario.horario"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('horario.object', {
#             'object': obj
#         })
