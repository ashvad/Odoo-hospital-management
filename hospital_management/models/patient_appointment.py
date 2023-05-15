# -*- coding: utf-8 -*-
from odoo import fields, models, api


class PatientAppointment(models.Model):
    """ for crating patient appointment """
    _name = 'patient.appointment'
    _description = 'patient appointment'
    _inherit = 'mail.thread'
    _rec_name = 'patient_card_id'

    patient_card_id = fields.Many2one('patient.card', string="Patient Card")
    patient_name_id = fields.Many2one('res.partner', string='Patient Name', related='patient_card_id.patient_name_id')
    doctor_id = fields.Many2one('hr.employee', string="Doctor", required=True)
    department_id = fields.Many2one(string="Department", related='doctor_id.department_id')
    date = fields.Date(string='Date', default=fields.Date.today())
    op_id = fields.Many2one('patient.op')
    token_no = fields.Char(string="Token no")
    state = fields.Selection([('draft', 'Draft'), ('appointment', 'Appointment'), ('op', 'OP'),
                                        ('cancel', 'cancelled')],
                             default='draft')
    op_count = fields.Integer(compute='compute_count')
    user_id = fields.Many2one('res.users', compute='_compute_userid', store=True)

    @api.depends('doctor_id')
    def _compute_userid(self):
        """ compute user id to store datas """
        if self.doctor_id:
            self.user_id = self.doctor_id.user_id.id

    def action_confirm(self):
        """ adding confirm button in patient appointment """
        self.write({'state': 'appointment'})

    def action_cancel(self):
        """ action for cancel appointment """
        self.write({'state': 'cancel'})

    def action_cancel_op(self):
        """ action for cancel button from op stage """
        self.write({'state': 'cancel'})

    def action_convert_to_op(self):
        """ action for appointment convert to op """
        self.state = 'op'
        op = self.op_id.create({
            'patient_card_id': self.patient_card_id.id,
            'doctor_id': self.doctor_id.id,
            'state': 'done'
        })
        self.op_id = op.id
        self.write({'token_no': op.token_no})
        return {
            'res_model': 'patient.op',
            'type': 'ir.actions.act_window',
            'res_id': op.id,
            'view_mode': 'form',
            'view_type': 'form',
        }

    def get_op(self):
        """ action to create smart button """
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'OPs',
            'view_mode': 'form',
            'res_model': 'patient.op',
            'context': "{'create':False}",
            'res_id': self.op_id.id,
            'domain': [('id', '=', self.op_id.id)]
        }

    def compute_count(self):
        """ computing op count """
        if self.op_id:
            self.op_count = 1
        else:
            self.op_count = 0
