{
    'name': 'Custom Action Menu',
    'version': '1.0',
    'depends': ['base', 'contacts'],  # Make sure dependencies are correct
    'data': [
        'security/ir.model.access.csv',
        'views/custom_action_menu.xml',
        'views/res_users_form_view.xml',
    ],
    'installable': True,  # Ensure this is set to True
    'application': True,  # If you want it to appear in the app menu
}

