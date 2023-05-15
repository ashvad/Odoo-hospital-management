from odoo import fields, models


class EstateProperty(models.Model):
    _name = "estate.name"
    _description = "estate.property"

    name = fields.Many2one('res.partner', required=True)
    description = fields.Text('description')
    postcode = fields.Char('postcode')
    date_availability = fields.Date('date availability', copy=False)
    expected_price = fields.Float(string='expected price', required=True)
    selling_price = fields.Float(string='selling price', readonly=True, copy=False)
    bedrooms = fields.Integer(string='bedrooms', default=2)
    living_area = fields.Integer(string='living area')
    facades = fields.Integer(string='facades')
    garage = fields.Boolean(string='garage')
    garden = fields.Boolean(string='garden')
    garden_area = fields.Integer(string='garden area')
    garden_orientation = fields.Selection(string='garden orientation',
                                          selection=[('north', 'north'), ('south', 'south'), ('east', 'east'),
                                                     ('west', 'west')])
