{
    'name': "POS Style Receipt",
    'summary': "Custom POS-style receipt layout for invoices",
    'description': "Implements a POS-style receipt layout for printing invoices.",
    'author': "Idris Eslam Idris",
    'website': "http://www.yourcompany.com",
    'category': 'Accounting',
    'version': '0.1',
    'depends': ['base', 'account' , 'barcodes'],
    'data': [
        'views/pos_receipt_report.xml',
        'reports/pos_receipt_template.xml',
    ],
    'demo': [],
}
