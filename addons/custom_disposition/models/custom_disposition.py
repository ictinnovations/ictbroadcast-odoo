from odoo import models, fields, api
import requests
import json
import logging
import urllib.parse

_logger = logging.getLogger(__name__)

class CustomDisposition(models.Model):
    _name = 'custom.disposition'
    _description = 'Custom Disposition'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')
    contact_ids = fields.One2many('res.partner', 'disposition_id', string='Contacts')  # Assuming res.partner is the contact model
    note = fields.Text(string='Note')

    @api.model
    def export_to_ictbroadcast(self):
        # Call get_broadcast_credentials from res.users
        service_url, api_token = self.env.user.get_broadcast_credentials()

        if not service_url or not api_token:
            _logger.error('Failed to fetch ICTBroadcast credentials.')
            return

        # Use the credentials for further processing
        _logger.info('Service URL: %s, API Token: %s', service_url, api_token)
        # Complete service URL for Disposition Create
        disposition_create_url = f'{service_url}rest/Disposition_Create'

        # Get the IDs of the selected records
        selected_ids = self.env.context.get('active_ids', [])
        # Fetch the records based on the selected IDs
        dispositions = self.search([('id', 'in', selected_ids)])

        # Log each record's data
        for disposition in dispositions:
            # prepare the disposition data
            disposition_data = {
                'name': disposition.name or '',
                'description': disposition.description or '',
                'remote_disp_id': disposition.id,
                'remote_module': 'odoo18'
            }

            payload = {
                'disposition': disposition_data
            }
            # Log the payload for debugging
            _logger.error('API Payload is %s', payload)

            # URL-encode the payload data
            query_params = {
                'disposition': json.dumps(disposition_data),
            }

            # Construct the full URL with query parameters
            encoded_url = f"{disposition_create_url}?{urllib.parse.urlencode(query_params)}"

            # Define the headers for authorization
            headers = {
                'Authorization': f'Bearer {api_token}',
            }

            try:
                # Send the GET request with query parameters
                response = requests.get(encoded_url, headers=headers, verify=False)

                # Log the API response
                _logger.error('API response is %s', response)
                if response.status_code == 200:
                    response_data = response.json()
                    _logger.info(
                        'Disposition exported successfully'
                    )
                    
                else:
                    _logger.error(
                        'Failed to export Disposition'
                    )
                    
            except Exception as e:
                _logger.exception(
                    'Error to export Disposition'
                )

            _logger.info(f"Disposition Exported: ID={disposition.id}, Name={disposition.name}, Description={disposition.description}")

        # Return an action to show a confirmation dialog
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Export Successful',
                'message': f'{len(dispositions)} dispositions have been exported to ICTBroadcast.',
                'type': 'success',  # types: success, warning, danger, info
                'sticky': False,   # False = disappears automatically
            },
        }


