# -*- coding: utf-8 -*-
from odoo import fields, models


class PatientTreatment(models.Model):
    """ Adding tree view inside patient consultation form """
    _name = 'patient.treatment'
    _description = 'patient treatment'

    medicine = fields.Char(string="Medicine")
    dose = fields.Char(string="Dose")
    days = fields.Char(string="Days")
    description = fields.Char(string="Description")
