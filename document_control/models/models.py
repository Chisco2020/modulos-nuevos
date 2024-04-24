# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError

READONLY_FIELD_STATES = {state: [('readonly', True)] for state in ['draft', 'open', 'done']}


class DocumentControl(models.Model):
    _name = 'document.control'
    _description = 'document.control'

    name = fields.Char(
        string="Control Number",
        required=True,
        copy=False,
        default=lambda self: _('New')
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        default=(lambda self: self.env.company),
        required=True,
        string='Company',
    )
    warehouse_id = fields.Many2one(
        comodel_name='stock.warehouse',
        string='Warehouse',
        required=True
    )
    date_document_control = fields.Datetime(
        required=True,
        states=READONLY_FIELD_STATES,
        default=fields.Datetime.now
    )
    state = fields.Selection(
        [
            ('draft', 'Draft'),
            ('delivery', 'In Delivery'),
            ('liquidation', 'Liquidation'),
            ('done', 'Done'),
        ],
        default='draft',
    )
    agent_id = fields.Many2one(
        comodel_name='res.users',
        string="Agent",
        required=True
    )
    responsible_id = fields.Many2one(
        comodel_name='res.users',
        string="Responsible",
        required=True
    )
    truck_plate = fields.Char(required=True)
    document_ids = fields.Many2many(
        comodel_name='account.move',
        string='Invoices',
        copy=False
    )
    total_cash = fields.Float(
        compute='_compute_total_operation',
        readonly=True,
        store=False,
    )
    total_transfer = fields.Float(
        compute='_compute_total_operation',
        readonly=True,
        store=False,
    )
    total_check = fields.Float(
        compute='_compute_total_operation',
        readonly=True,
        store=False,
    )
    total = fields.Float(
        compute='_compute_total_operation',
        readonly=True,
        store=False,
    )
    total_due = fields.Float(
        compute='_compute_total_operation',
        readonly=True,
        store=False,
    )
    diference = fields.Float(
        compute='_compute_total_operation',
        readonly=True,
        store=False,
    )

    @api.depends('document_ids')
    def _compute_total_operation(self):
        for rec in self:
            total_cash = 0
            total_transfer = 0
            total_check = 0
            balance = 0
            total = 0
            for curr in rec.document_ids:
                total += curr.amount_total_signed

            for inv in rec.document_ids.ids:
                query_payment_move = self.get_query_payment_move()
                rec._cr.execute(
                    query_payment_move,
                    [inv],
                )
                payment = self._cr.dictfetchone()
                if payment:
                    if payment['type'] == 'transfer':
                        total_transfer += payment['amount']
                    if payment['type'] == 'cash':
                        total_cash += payment['amount']
                    if payment['type'] == 'check':
                        total_check += payment['amount']
                    balance += payment['balance']

            diference = total - balance

            rec.total_cash = total_cash
            rec.total_transfer = total_transfer
            rec.total_check = total_check
            rec.total = total
            rec.total_due = balance
            rec.diference = diference

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _("New")) == _("New"):
                vals['name'] = self.env['ir.sequence'].next_by_code('document.control') or _("New")

        return super().create(vals_list)

    def action_to_delivery(self):
        self.state = 'delivery'

    def action_to_liquidation(self):
        self.state = 'liquidation'

    def action_to_done(self):
        balance = 0
        amount = 0
        for rec in self.document_ids:
            amount += rec.amount_total_signed

        for inv in self.document_ids.ids:
            query_payment_move = self.get_query_payment_move()
            self._cr.execute(
                query_payment_move,
                [inv],
            )
            payment = self._cr.dictfetchone()
            if payment:
                balance += payment['balance']
        if amount - balance != 0:
            raise UserError(
                _(
                    "You cannot go to done because the difference between the amounts and payments is not equal to '0'"
                )
            )
        else:
            self.state = 'done'

    def action_delivery_of_documents_for_collection(self):
        return self.env.ref('document_control.action_document_for_collection_report').report_action(
            self
        )

    def action_print_report_doc_ctrl(self):
        return self.env.ref('document_control.action_document_control_liquidation').report_action(
            self
        )

    def get_query_payment_move(self):
        query_payment_move = """
                SELECT
                payment.amount AS balance,invoice.amount_total_signed AS amount, payment.payment_type_doc_control AS type
                FROM account_payment payment
                JOIN account_move move ON move.id = payment.move_id
                JOIN account_move_line line ON line.move_id = move.id
                JOIN account_partial_reconcile part ON
                    part.debit_move_id = line.id
                    OR
                    part.credit_move_id = line.id
                JOIN account_move_line counterpart_line ON
                    part.debit_move_id = counterpart_line.id
                    OR
                    part.credit_move_id = counterpart_line.id
                JOIN account_move invoice ON invoice.id = counterpart_line.move_id
                JOIN account_account account ON account.id = line.account_id
                JOIN account_journal journal ON journal.id = move.journal_id
                WHERE account.account_type IN ('asset_receivable', 'liability_payable')
                    AND invoice.id= %s
                    AND line.id != counterpart_line.id
                    AND invoice.move_type in ('out_invoice', 'out_refund',
                    'in_invoice', 'in_refund', 'out_receipt', 'in_receipt')
                GROUP BY payment.amount,invoice.amount_total_signed,payment.payment_type_doc_control
                                        """
        return query_payment_move


class AccountMove(models.Model):
    _inherit = 'account.move'

    partner_vat = fields.Char(related='partner_id.vat')
    partner_phone = fields.Char(related='partner_id.phone')
    partner_mobile = fields.Char(related='partner_id.mobile')
    partner_email = fields.Char(related='partner_id.email')
    partner_user_name = fields.Char(related='partner_id.user_id.name', string='Sales Person')
    partner_zones = fields.Char(related='partner_id.category_id.name', string='Zone')

    def get_data_payment_qweb(self):
        total_bank = 0
        total_cash = 0
        total_check = 0
        receipt = False
        self._cr.execute(
            """
            SELECT
            payment.id AS payment_id, ARRAY_AGG(DISTINCT invoice.id) AS invoice_ids,
            invoice.move_type AS move_type, payment.amount AS amount,move.journal_id AS move_id,
            journal.name AS journal_name, payment.amount AS amount,
            payment.payment_type_doc_control AS type, payment.receipt_number AS receipt
            FROM account_payment payment
            JOIN account_move move ON move.id = payment.move_id
            JOIN account_move_line line ON line.move_id = move.id
            JOIN account_partial_reconcile part ON
                part.debit_move_id = line.id
                OR
                part.credit_move_id = line.id
            JOIN account_move_line counterpart_line ON
                part.debit_move_id = counterpart_line.id
                OR
                part.credit_move_id = counterpart_line.id
            JOIN account_move invoice ON invoice.id = counterpart_line.move_id
            JOIN account_account account ON account.id = line.account_id
            JOIN account_journal journal ON journal.id = move.journal_id
            WHERE account.account_type IN ('asset_receivable', 'liability_payable')
                AND invoice.id= %s
                AND line.id != counterpart_line.id
                AND invoice.move_type in ('out_invoice', 'out_refund', 'in_invoice',
                'in_refund', 'out_receipt', 'in_receipt')
            GROUP BY payment.id, invoice.move_type, payment.amount,move.journal_id,
            journal.name, payment.amount, payment.payment_type_doc_control
            """,
            [self.id],
        )
        payment = self._cr.dictfetchone()

        if payment:
            if payment['type'] == 'transfer':
                total_bank = payment['amount']
            if payment['type'] == 'cash':
                total_cash = payment['amount']
            if payment['type'] == 'check':
                total_check = payment['amount']
            receipt = payment['receipt']
        data = {
            'total_bank': total_bank,
            'total_cash': total_cash,
            'total_check': total_check,
            'receipt_number': receipt if receipt else '-',
        }
        return data
