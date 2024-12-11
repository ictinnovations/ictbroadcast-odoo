from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class CustomDisposition(models.Model):
    _name = 'custom.disposition'
    _description = 'Custom Disposition'

    name = fields.Char(string='Name', required=True)
    description = fields.Text(string='Description')

    @api.model
    def export_to_ictbroadcast(self):
        # Get the IDs of the selected records
        selected_ids = self.env.context.get('active_ids', [])
        # Fetch the records based on the selected IDs
        dispositions = self.search([('id', 'in', selected_ids)])

        # Log each record's data
        for disposition in dispositions:
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

