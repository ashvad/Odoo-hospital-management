# -*- coding: utf-8 -*-

from odoo import fields, models, api


class HrEmployee(models.Model):
    _inherit = ['hr.employee']
    is_doctor = fields.Boolean(string="Is Doctor")
    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    fee = fields.Monetary(string="Fee")

    @api.onchange('is_doctor')
    def onchange_is_doctor(self):
        """ Job position filtered by is_doctor = True """
        if self.is_doctor:
            data = self.env['hr.job'].search([('name', 'like', 'Doctor')])
            self.write({'job_id': data.id})
        else:
            store = self.env['hr.job'].search([('name', 'like', 'Chief Technical Officer')])
            self.write({'job_id': store.id})
