from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    disposition_id = fields.Many2one('custom.disposition', string='Disposition')

