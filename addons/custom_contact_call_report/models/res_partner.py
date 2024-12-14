from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    call_status = fields.Selection([
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ], string="Call Status")

    call_response = fields.Char(string="Call Response")
    destination_name = fields.Char(string="Destination Name")
    call_amount = fields.Float(string="Amount")

