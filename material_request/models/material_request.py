# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class MaterialRequest(models.Model):
    """ creating material request """
    _name = 'material.request'
    _description = 'material request'
    _inherit = 'mail.thread'
    _rec_name = 'request_number'

    request_number = fields.Char(string="Request Number", required="True", default=lambda self: _('New'))
    date = fields.Date(string="Date", required="True", default=fields.date.today())
    requested_by_id = fields.Many2one('res.users', string="Requested By", required="True",
                                      default=lambda self: self.env.user, readonly=True)
    email = fields.Char(string="Email", related='requested_by_id.login')
    language = fields.Selection(string="Language", related='requested_by_id.lang')
    mobile = fields.Char(string="Mobile")
    product_ids = fields.One2many('material.product', 'material_id', string="order line")
    state = fields.Selection(
        selection=[('draft', 'draft'), ('submit', 'submit'), ('to_approve', 'to approve'), ('approve', 'Approved'),
                   ('reject', 'rejected')], default='draft')
    tz = fields.Selection(string="TimeZone", related='requested_by_id.tz')
    purchase_ids = fields.Many2many('purchase.order')
    stock_ids = fields.Many2many('stock.picking')
    rfq_count = fields.Integer(string="RFQ")
    it_count = fields.Integer(string="Internal Transfer")

    @api.model
    def create(self, vals):
        """ creating request number """
        if vals.get('request_number', _('New')) == _('New'):
            vals['request_number'] = self.env['ir.sequence'].next_by_code(
                'material.request') or _('New')
        return super(MaterialRequest, self).create(vals)

    def action_submit(self):
        """ adding confirm button"""
        self.write({'state': 'submit'})

    def action_approve(self):
        """ adding approve button """
        self.write({'state': 'to_approve'})

    def action_rejection(self):
        """ adding rejection button """
        self.write({'state': 'reject'})

    def action_get_purchase(self):
        """ adding purchase smart tab """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'RFQ',
            'view_mode': 'tree,form',
            'res_model': 'purchase.order',
            'context': "{'create':False}",
            'domain': [('id', 'in', self.purchase_ids.ids)]
        }

    def action_get_it(self):
        """ adding internal transfer smart tab """
        self.ensure_one()
        record = self.stock_ids.search([('origin', '=', self.request_number)]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Internal Transfer',
            'view_mode': 'tree,form',
            'res_model': 'stock.picking',
            'context': "{'create': False}",
            'domain': [('id', 'in', record)],
        }

    def action_to_approve(self):
        """ adding a button to approve the request """
        self.write({'state': 'approve'})
        for rec in self.product_ids:
            if rec.type == 'po':
                for vendor in rec.product_id.seller_ids:
                    store = self.env['purchase.order'].create({
                        'partner_id': vendor.partner_id.id,
                        'origin': self.request_number,
                        'order_line': [fields.Command.create({
                            'product_id': rec.product_id.id,
                            'product_qty': rec.quantity
                        })]
                    })
                    self.purchase_ids = [fields.Command.link(store.id)]
                    self.rfq_count = len(self.purchase_ids)
            elif rec.type == "it":
                record = self.env['stock.picking'].create({
                    'picking_type_id': self.env.ref('stock.picking_type_internal').id,
                    'origin': self.request_number,
                    'location_id': rec.source_location.id,
                    'location_dest_id': rec.destination_loc.id,
                    'move_ids': [fields.Command.create({
                        'product_id': rec.product_id.id,
                        'product_uom_qty': rec.quantity,
                        'location_id': rec.source_location.id,
                        'location_dest_id': rec.destination_loc.id,
                        'name': self.requested_by_id.id
                    })]
                })
                self.stock_ids = [fields.Command.link(record.id)]
                self.it_count = len(self.stock_ids)
