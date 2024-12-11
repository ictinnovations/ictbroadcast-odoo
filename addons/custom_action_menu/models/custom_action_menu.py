from odoo import models, fields, api
import requests
import json
import logging
import urllib.parse

_logger = logging.getLogger(__name__)

class CustomActionMenu(models.Model):
    _name = 'custom.action.wizard'  # Define a new model
    _description = 'Custom Action Wizard'

    # Dropdown field
    campaign_id = fields.Selection(
        selection='get_campaigns',
        string='Select Campaign',
        required=True
    )

    # Many2many field to store selected contacts
    contact_ids = fields.Many2many(
        'res.partner',
        string='Selected Contacts',
        readonly=True
    )

    def get_broadcast_credentials(self):
        """Fetch ICTBroadcast credentials from the current user."""
        # Access the current user
        current_user = self.env.user

        # Retrieve the ICTBroadcast URL and Access Key from the current user's fields
        service_url = current_user.ictbroadcast_url
        api_token = current_user.ictbroadcast_access_key

        if not service_url or not api_token:
            _logger.error('ICTBroadcast URL or Access Key is not set for the current user.')
            return None, None

        # Ensure the service URL ends with a slash
        if not service_url.endswith('/'):
            service_url += '/'

        _logger.error('url and token is  %s: %s', service_url, api_token)
        return service_url, api_token

    @api.model
    def get_campaigns(self):
        """Fetch campaigns from the external API and return them as a list of tuples."""
        # Get the ICTBroadcast credentials
        service_url, api_token = self.get_broadcast_credentials()
        if not service_url or not api_token:
            return []

        # Complete service URL for Campaign List Mode
        campaign_list_url = f'{service_url}rest/Campaign_List_Mode'

        try:
            headers = {'Authorization': f'Bearer {api_token}'}
            payload = {'status': ''}  # Send any required parameters
            response = requests.post(campaign_list_url, headers=headers, data=payload, verify=False)

            # Log the response
            _logger.info('API Response: %s', response.text)

            if response.status_code == 200:
                data = response.json()  # Parse JSON response

                # Extract campaigns from the second element of the list
                if isinstance(data, list) and len(data) > 1 and isinstance(data[1], list):
                    campaigns = [
                        (str(campaign['campaign_id']), campaign['name'])
                        for campaign in data[1]
                    ]
                    return campaigns
                else:
                    _logger.error('Unexpected API response format: %s', data)
                    return []
            else:
                _logger.error('API Request failed with status %s: %s', response.status_code, response.text)
                return []
        except Exception as e:
            _logger.exception('Error while calling API: %s', e)
            return []

    def confirm_action(self):
        """Handle the confirm button click and load contacts into the campaign."""
        # Get the ICTBroadcast credentials
        service_url, api_token = self.get_broadcast_credentials()
        if not service_url or not api_token:
            return

        # Complete service URL for Campaign Contact Create
        contact_create_url = f'{service_url}rest/Campaign_Contact_Create'

        # Get the selected campaign
        campaign_id = self.campaign_id
        if not campaign_id:
            _logger.error("No campaign selected.")
            return

        success_contacts = []  # List to track successfully exported contacts
        failed_contacts = []  # List to track failed contacts
    
        # Iterate over each selected contact
        for contact in self.contact_ids:
            # Prepare the contact data
            contact_data = {
                'first_name': contact.name.split(' ')[0] if ' ' in contact.name else contact.name,
                'last_name': contact.name.split(' ')[1] if ' ' in contact.name else '',
                'phone': contact.phone or contact.mobile or '',
                'address': contact.street or 'N/A',
                'email': contact.email or '',
            }

            # Prepare the remote data
            remote_data = {
                'remote_id': str(contact.id),
                'remote_module': 'Contact'
            }

            # Combine everything into the payload
            payload = {
                'contact': contact_data,
                'campaign_id': campaign_id,
                'schedule_time': '',
                'expiry': '',
                'remote': remote_data
            }

            # Log the payload for debugging
            _logger.error('API Payload is %s', payload)

            # URL-encode the payload data
            query_params = {
                'contact': json.dumps(contact_data),
                'campaign_id': str(campaign_id),
                'schedule_time': '',
                'expiry': '',
                'remote': json.dumps(remote_data)
            }

            # Construct the full URL with query parameters
            encoded_url = f"{contact_create_url}?{urllib.parse.urlencode(query_params)}"

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
                        'Contact %s (%s) added to Campaign %s successfully: %s',
                        contact.name,
                        contact.email,
                        campaign_id,
                        response_data
                    )
                    success_contacts.append(contact.name)  # Track successful contact
                else:
                    _logger.error(
                        'Failed to add contact %s (%s) to Campaign %s: %s',
                        contact.name,
                        contact.email,
                        campaign_id,
                        response.text
                    )
                    failed_contacts.append(contact.name)  # Track failed contact
            except Exception as e:
                _logger.exception(
                    'Error adding contact %s (%s) to Campaign %s: %s',
                    contact.name,
                    contact.email,
                    campaign_id,
                    str(e)
                )
                failed_contacts.append(contact.name)  # Track failed contact

        # Prepare success message
        message = f"{', '.join(success_contacts)} exported to Campaign {campaign_id} successfully."

        # Optionally, include failed contacts in the message
        if failed_contacts:
            message += f"\nFailed to export: {', '.join(failed_contacts)}."

        # Display the notification message
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Export Status',
                'message': message,
                'type': 'success' if not failed_contacts else 'warning',  # Success if no failures, else warning
                'sticky': False,  # Disappear automatically
            },
        }, {
            'type': 'ir.actions.act_window',
            'res_model': 'res.partner',
            'view_mode': 'list',
            'target': 'current',
        }


    @api.model
    def custom_action_function(self):
        """Handle the custom action."""
        return {
            'type': 'ir.actions.act_window',
            'name': 'Custom Action',
            'view_mode': 'form',
            'res_model': 'custom.action.wizard',
            'target': 'new',
        }

