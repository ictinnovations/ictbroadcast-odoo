# models/res_partner.py
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    do_not_call = fields.Boolean(string="Do Not Call", default=False)
