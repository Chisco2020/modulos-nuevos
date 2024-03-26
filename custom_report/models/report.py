from odoo import models, fields

# Purchase Order Line Customizations
class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    custom_field1 = fields.Char('Custom Field 1')
    custom_field2 = fields.Boolean('Checkbox Field 2')
    custom_field3 = fields.Boolean('Checkbox Field 3')
    bultos_no_cargados = fields.Char('Bultos No Cargados')

# Sale Order Line Customizations
class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    custom_field1 = fields.Char('Custom Field 1')
    custom_field2 = fields.Boolean('Checkbox Field 2')
    custom_field3 = fields.Boolean('Checkbox Field 3')
    bultos_no_cargados = fields.Char('Bultos No Cargados')

# Purchase Order Customizations
class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    custom_field1 = fields.Char('Custom Field 1')
    custom_field2 = fields.Boolean('Checkbox Field 2')
    custom_field3 = fields.Boolean('Checkbox Field 3')
    bultos_no_cargados = fields.Char('Bultos No Cargados')
    enlisted_signature = fields.Char('Enlisted Signature')
    delivery_signature = fields.Char('Signature Delivery')
    received_signature = fields.Char('Signature Received')

# Sale Order Customizations
class SaleOrder(models.Model):
    _inherit = 'sale.order'

    custom_field1 = fields.Char('Custom Field 1')
    custom_field2 = fields.Boolean('Checkbox Field 2')
    custom_field3 = fields.Boolean('Checkbox Field 3')
    bultos_no_cargados = fields.Char('Bultos No Cargados')
    enlisted_signature = fields.Char('Enlisted Signature')
    delivery_signature = fields.Char('Signature Delivery')
    received_signature = fields.Char('Signature Received')
