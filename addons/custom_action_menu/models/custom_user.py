from odoo import models, fields

class ResUsers(models.Model):
    _inherit = 'res.users'

    # New fields for ICTBroadcast URL and Access Key
    ictbroadcast_url = fields.Char(string='ICTBroadcast URL', help="The URL for the ICTBroadcast API.")
    ictbroadcast_access_key = fields.Char(string='ICTBroadcast Access Key', help="The Access Key for the ICTBroadcast API.")

