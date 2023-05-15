# -*- coding: utf-8 -*-

from odoo import fields, models


class PatientDisease(models.Model):
    """ storing patient diseases datas """
    _name = 'patient.disease'
    _description = 'patient disease'
    _rec_name = "disease"

    disease = fields.Char(string="Disease")
