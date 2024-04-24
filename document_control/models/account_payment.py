# -*- coding: utf-8 -*-
from odoo import fields, models


class AccountPaymentRegister(models.TransientModel):
    _inherit = 'account.payment.register'

    receipt_number = fields.Char(required=True)

    payment_type_doc_control = fields.Selection(
        [
            ('none', 'None'),
            ('check', 'Check'),
            ('transfer', 'Transfer'),
            ('cash', 'Cash')
        ],
        default='none'
    )

    def _create_payments(self):
        res = super()._create_payments()
        res.receipt_number = self.receipt_number
        res.payment_type_doc_control = self.payment_type_doc_control
        return res


class AccountPayment(models.Model):
    _inherit = 'account.payment'

    receipt_number = fields.Char()

    payment_type_doc_control = fields.Selection(
        [
            ('none', 'None'),
            ('check', 'Check'),
            ('transfer', 'Transfer'),
            ('cash', 'Cash')
        ],
        default='none'
    )
