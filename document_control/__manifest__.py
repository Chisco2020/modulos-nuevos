# -*- coding: utf-8 -*-
{
    'name': "Document Control",
    'summary': """
        Extension of the account module to control documents
        handed over to the drivers.""",
    'license': "Other proprietary",
    'author': "Sistemas En Linea",
    'website': "https://www.sistemas-en-linea.com",
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customizations',
    'version': '16.0.1.0.0',
    # any module necessary for this one to work correctly
    'depends': ['base', 'account', 'stock'],
    # always loaded
    'data': [
        'security/doc_control_security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'reports/paper_format.xml',
        'reports/report_document_control_template.xml',
        'reports/report_menu.xml',
        'views/views.xml',
        'views/account_payment.xml',
    ],
}
