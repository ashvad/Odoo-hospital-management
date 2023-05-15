# -*- coding: utf-8 -*-

from datetime import date

from odoo import fields, models, api, _


# Patient details Model

class PatientCard(models.Model):
    """ Patient Details"""
    _name = "patient.card"
    _description = "patient.card"
    _rec_name = 'patient'
    _inherit = 'mail.thread'

    patient = fields.Char(string="Patient ID", required="True", default=lambda self: _('New'), readonly=True)
    patient_name_id = fields.Many2one('res.partner', string="Patient Name", required=True)
    dob = fields.Date(string="DOB", related='patient_name_id.dob')
    age = fields.Integer(string="Age")
    gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string="Blood Group",
                              related='patient_name_id.gender')
    mobile = fields.Char(string="Mobile", related='patient_name_id.mobile')
    phone = fields.Char(string="Phone", related='patient_name_id.phone')
    blood_group = fields.Selection([('A+', 'A+'), ('B+', 'B+'), ('o+', 'o+'), ('AB-', 'AB-'), ('o-', 'o-'),
                                    ('A-', 'A-')], string="Blood Group")
    op_history_ids = fields.One2many('patient.op', 'patient_card_id', string="OP History")
    state = fields.Selection(
        [('draft', 'Draft'), ('done', 'Confirm'), ('appointment', 'Appointment'), ('cancel', 'cancelled')],
        default='draft')
    appointment_count = fields.Integer(compute='compute_count')
    appointment_id = fields.Many2one('patient.appointment')
    sale_order_id = fields.Many2one('sale.order', string='sale')

    @api.model
    def create(self, vals):
        """ Patient reference number"""
        if vals.get('patient', _('New')) == _('New'):
            vals['patient'] = self.env['ir.sequence'].next_by_code(
                'patient.sequence') or _('New')
        return super(PatientCard, self).create(vals)

    @api.onchange("dob")
    def onchange_patient_dob(self):
        """" calculating patient age """
        if self.dob:
            today = date.today().year
            born = self.dob.year
            self.age = today - born

    def action_create_appointment(self):
        """ adding a create button in patient card """
        self.write({'state': 'appointment'})
        return {
            'res_model': 'patient.appointment',
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'context': {'default_patient_card_id': self.id}
        }

    def action_confirm(self):
        """ adding confirm button in patient card """
        self.write({'state': 'done'})
        # self.sale_order_id.state = 'sale'
        # .country_id.name.partner_id
        # rec = self.sale_order_id.order_line.product_template_id.seller_ids.partner_id
        # for i in rec:
        #     print(i.country_id.name)
            # print(i.name)

    def action_cancel(self):
        """ cancelling patient card from confirm stage """
        self.write({'state': 'cancel'})

    def action_cancel_appointment(self):
        """ cancelling from appointment stage """
        self.write({'state': 'cancel'})

    def get_app(self):
        """ adding details in smart tab """
        self.ensure_one()
        store = self.appointment_id.search([('patient_card_id', '=', self.id)]).ids
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'view_mode': 'tree,form',
            'res_model': 'patient.appointment',
            'context': "{'create':False}",
            'domain': [('id', 'in', store)]
        }

    def compute_count(self):
        """ calculating appointment count """
        for record in self:
            record.appointment_count = self.appointment_id.search_count(
                [('patient_card_id', '=', self.id)])
