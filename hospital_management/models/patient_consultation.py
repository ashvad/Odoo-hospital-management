# -*- coding: utf-8 -*-

from odoo import fields, models


class PatientConsultation(models.Model):
    """ Patient Consultation """
    _name = "patient.consultation"
    _description = "patient consultation"
    _inherit = 'mail.thread'
    _rec_name = 'patient_card_id'

    # def _op_domain(self):
    #     return [('patient_card_id.id', '=', self.patient_card_id.id)]

    patient_card_id = fields.Many2one('patient.card', string="Patient Card", required=True)
    consultation_type = fields.Selection(string="Consultation Type", selection=[('OP', 'OP'), ('IP', 'IP')],
                                         required=True)
    doctor_id = fields.Many2one('hr.employee', string="Doctor", required=True)
    department_id = fields.Many2one(string="Department", related='doctor_id.department_id')
    date = fields.Date(string="Date", default=fields.Date.today())
    disease_id = fields.Many2one('patient.disease', string="Disease")
    diagnose = fields.Text(string="Diagnose")
    treatment_ids = fields.Many2many('patient.treatment', string="Treatment")
    op_id = fields.Many2one('patient.op', string='OP', required=True)
