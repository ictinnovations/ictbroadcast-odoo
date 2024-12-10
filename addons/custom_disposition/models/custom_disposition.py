from odoo import models, fields

class CustomDisposition(models.Model):
    _name = 'custom.disposition'
    _description = 'Custom Disposition'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

