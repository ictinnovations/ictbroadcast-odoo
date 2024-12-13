from odoo import models, fields

class ResPartnerCall(models.Model):
    _name = 'res.partner.call'
    _description = 'Contact Call Details'

    partner_id = fields.Many2one('res.partner', string='Contact', required=True, ondelete='cascade')
    callstart = fields.Char(string='Call Start')
    callconnect = fields.Char(string='Call Connected')
    destination = fields.Char(string='Destination Name')
    status = fields.Char(string='Status', required=True)
    amount = fields.Float(string='Amount')
    response = fields.Text(string='Response')
    