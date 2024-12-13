from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    call_report_ids = fields.One2many('res.partner.call', 'partner_id', string='Call Reports')
