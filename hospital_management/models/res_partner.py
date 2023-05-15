# -*- coding: utf-8 -*-

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    dob = fields.Date(string="DOB")
    gender = fields.Selection(selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')])
