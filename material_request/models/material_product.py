# -*- coding: utf-8 -*-
from odoo import fields, models, api


class MaterialProduct(models.Model):
    """ creating order line fields """
    _name = 'material.product'
    _description = 'material product'

    product_id = fields.Many2one('product.product', string="Product", required=True)
    description = fields.Char(string="Description", related='product_id.name')
    quantity = fields.Float(string="Quantity", default='1')
    material_id = fields.Many2one('material.request')
    type = fields.Selection(selection=[('it', 'Internal Transfer'), ('po', 'RFQ')], required=True)
    source_location = fields.Many2one('stock.location', string='Source Location')
    destination_loc = fields.Many2one('stock.location', string='Destination Location')
