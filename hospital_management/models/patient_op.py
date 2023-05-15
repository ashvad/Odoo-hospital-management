# -*- coding: utf-8 -*-
from odoo import fields, models, api, _


class PatientOP(models.Model):
    """ creating patient op tickets"""

    _name = "patient.op"
    _description = "patient.op.tickets"
    _rec_name = 'token_no'
    _inherit = 'mail.thread'

    patient_card_id = fields.Many2one('patient.card', string="Patient Card", required=True)
    patient_name_id = fields.Many2one('res.partner', string="Patient Name", related='patient_card_id.patient_name_id',
                                      store=True)
    age = fields.Integer(string="Age", related='patient_card_id.age')
    gender = fields.Selection(string="Gender", selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
                              related='patient_card_id.gender')
    blood_group = fields.Selection(string="Blood Group",
                                   selection=[('A+', 'A+'), ('B+', 'B+'), ('o+', 'o+'), ('AB-', 'AB-'), ('o-', 'o-'),
                                              ('A-', 'A-')], related='patient_card_id.blood_group')
    doctor_id = fields.Many2one('hr.employee', string="Doctor", required=True)
    date = fields.Date(string="Date", default=fields.Date.today())
    token_no = fields.Char(string="Token No", default=lambda self: _('New'), readonly=True)

    company_id = fields.Many2one('res.company', copy=False,
                                 string="Company",
                                 default=lambda self: self.env.user.company_id.id)
    account_id = fields.Many2one('account.move')
    invoice_count = fields.Integer(compute='compute_count')

    currency_id = fields.Many2one('res.currency', string="Currency",
                                  related='company_id.currency_id',
                                  default=lambda self: self.env.user.company_id.currency_id.id)
    fee = fields.Monetary(string="Fee", related='doctor_id.fee')
    department_id = fields.Many2one(string="Department", related='doctor_id.department_id', store=True)
    state = fields.Selection(
        selection=[
            ('draft', "Draft"),
            ('done', "OP"),
            ('cancel', 'Cancelled'),
            ('paid', 'paid')
        ],
        default='draft')

    def action_confirm(self):
        """ adding confirm button in patient op """
        self.write({'state': 'done'})

    def action_cancel(self):
        """ cancelling op tickets """
        self.write({'state': 'cancel'})

    @api.model
    def create(self, vals):
        """ creating patient op token """
        if vals.get('token_no', _('New')) == _('New'):
            vals['token_no'] = self.env['ir.sequence'].next_by_code(
                'OP.Token') or _('New')
        return super(PatientOP, self).create(vals)

    def action_token_no_recurring(self):
        """ Token number daily recurring """
        sequence = self.env.ref('hospital_management.patient_token_no')
        sequence.write({'number_next_actual': 1})

    def action_fee(self):
        """ creating invoice """
        self.write({'state': 'paid'})
        invoice = self.env['account.move'].create({
            'partner_id': self.patient_name_id.id,
            'invoice_origin': self.patient_card_id.patient,
            'move_type': 'out_invoice',
            'invoice_line_ids': [fields.Command.create({
                'name': self.doctor_id.name,
                'price_unit': self.fee,
                'quantity': 1.0,
            })]
        })
        self.account_id = invoice.id
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'res_id': self.account_id.id,

        }

    def get_payment(self):
        """ adding smart button """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoice',
            'view_mode': 'form',
            'res_model': 'account.move',
            'context': "{'create':'False'}",
            'res_id': self.account_id.id
        }

    def compute_count(self):
        """ counting the invoice """
        if self.account_id:
            self.invoice_count = 1
        else:
            self.invoice_count = 0
