from odoo import fields, models


class Selection(models.Model):
    _name = 'selection.view'

    select = fields.Selection(string='Resistance', selection=[('pass', 'pass'), ('fail', 'fail')])
