{
    'name': 'Custom Contact Call Report',
    'version': '1.0',
    'depends': ['base', 'contacts'],
    'license': 'LGPL-3',
    'data': [
        'views/contact_report_views.xml',
        'views/contact_report_menu.xml',
    ],
    'installable': True,  # Ensure this is set to True
    'application': True,  # If you want it to appear in the app menu
}
