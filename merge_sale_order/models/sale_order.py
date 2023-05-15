# -*- coding: utf-8 -*-
from odoo import fields, models, api


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_confirm(self):
        """"""
        for rec in self.order_line:
            line_ids = self.order_line.filtered(
                lambda
                    l: l.product_template_id.id == rec.product_template_id.id and l.price_unit == rec.price_unit)
            if rec.id in line_ids.mapped('id')[1:]:
                rec.unlink()
                continue
            else:
                quantity = 0
                for qty in line_ids:
                    quantity += qty.product_uom_qty
                line_ids.write({'price_unit': rec.price_unit, 'product_uom_qty': quantity,
                                'order_id': line_ids.order_id.id})
        return super(SaleOrder, self).action_confirm()


