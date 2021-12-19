# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Vender(models.Model):
    _name = 'vender'
    _description = 'Vender Details'

    name = fields.Char()

class marbleshope(models.Model):
    _name = 'marble'
    _description = 'Marble data'
    # _sql_constraints = [('isbn_unique', 'unique(isbn)', 'Duplicate isbn not allowed')]
    # _order = 'price desc'

    name = fields.Char(string="Vender Name", default="Unknown", required=True)
    # book_description = fields.Text()
    product = fields.Text()
    # price = fields.Float()
    qnt = fields.Float()
    nom = fields.Float()
    unitprice = fields.Float()
    totalprice = fields.Float()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
