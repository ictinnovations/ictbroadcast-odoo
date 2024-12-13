{
    'name': 'Custom Contact Report',
    'version': '1.0',
    'depends': ['base', 'contacts'],
    'license': 'LGPL-3',
    'data': [
        'security/ir.model.access.csv',
        'views/custom_contact_report_view.xml',
    ],
    'installable': True,  # Ensure this is set to True
    'application': True,  # If you want it to appear in the app menu
}
