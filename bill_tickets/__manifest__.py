{
    'name': "POS Style Receipt",
    'summary':
        """
        Custom POS-style receipt layout for invoices

        Implements a POS-style receipt layout for printing invoices.
        """,
    'author': "Idris Eslam Idris",
    'license': "",
    'category': 'Accounting',
    'version': '16.0.0.0.1',
    'depends': [
        'base',
        'account',
        'barcodes'
    ],
    'data': [
        'views/pos_receipt_report.xml',
        'reports/pos_receipt_template.xml',
    ],
    'demo': [],
}
