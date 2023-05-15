from odoo import fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order.line'

    milestone = fields.Integer(string='Milestone', default=1)
