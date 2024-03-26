{
    'name': 'custom report v16',
    'version': '1.0',
    'category': 'Customization',
    'summary': 'Customization for Purchase Order and Sales Order reports for Version 16',
    'author': 'MZN, Idris Eslam Idris',
    'description': """
        Add custom fields, checkboxes, and signatures to Purchase Order and Sales Order reports.
    """,
    'depends': ['base', 'purchase', 'sale'],
    'data': [
                'views/purchase_report_inherit.xml',

    ],
    'installable': True,
    'application': False,
}
