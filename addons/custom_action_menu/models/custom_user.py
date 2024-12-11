from odoo import models, fields
import logging

_logger = logging.getLogger(__name__)

class ResUsers(models.Model):
    _inherit = 'res.users'

    # New fields for ICTBroadcast URL and Access Key
    ictbroadcast_url = fields.Char(string='ICTBroadcast URL', help="The URL for the ICTBroadcast API.")
    ictbroadcast_access_key = fields.Char(string='ICTBroadcast Access Key', help="The Access Key for the ICTBroadcast API.")

    def get_broadcast_credentials(self):
        """Fetch ICTBroadcast credentials for the current user."""
        # Access the current user
        current_user = self.env.user

        # Retrieve the ICTBroadcast URL and Access Key from the current user's fields
        service_url = current_user.ictbroadcast_url
        api_token   = current_user.ictbroadcast_access_key

        if not service_url or not api_token:
            _logger.error('ICTBroadcast URL or Access Key is not set for the current user.')
            return None, None

        # Ensure the service URL ends with a slash
        if not service_url.endswith('/'):
            service_url += '/'

        _logger.info('Service URL: %s, API Token: %s', service_url, api_token)
        return service_url, api_token
