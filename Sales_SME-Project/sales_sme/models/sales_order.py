import typing

from odoo import models, fields, api
from odoo.exceptions import UserError
from odoo.orm.types import ValuesType


class SalesOrder(models.Model):
    _name = "sales.order"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Sales Order"
    name = fields.Char(string='Order', default='New', tracking=True)
    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    date_order = fields.Datetime(string='Date', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancel', 'Cancelled'),
    ], default='draft', string='State', tracking=True)
    order_line = fields.One2many('sales.order.line', 'order_id', string='Order Lines')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    total_amount_new = fields.Float(string='Total Amount Change', compute='_compute_total_amount_new', store=True)
    @api.onchange('order_line.quantity', 'order_line.price_unit')
    def _compute_total_amount_new(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.order_line)
    @api.depends('order_line.quantity', 'order_line.price_unit')
    def _compute_total_amount(self):
        for order in self:
            order.total_amount = sum(line.subtotal for line in order.order_line)
    def action_draft(self):
        for order in self:
            order.state = 'draft'
    def action_confirm(self):
        for order in self:
            if order.state != 'draft':
                continue
            order.state = 'confirmed'
            order.message_post(
                body = "Sales Order has been confirmed"
            )
            order.activity_schedule(
                'mail.mail_activity_data_todo',
                summary = "Prepare order for processing"
            )
    def action_done(self):
        for order in self:
            order.state = 'done'
    def action_cancel(self):
        for order in self:
            order.state = 'cancel'
    @api.model
    def create(self, vals):
        res = super(SalesOrder, self).create(vals)
        if res.name == 'New':
            res.name = self.env['ir.sequence'].next_by_code('sales_order_sequence')
        return res
    @api.model
    def write(self, vals):
        for order in self:
            if order.state in ('confirmed', 'done'):
                forbidden_fields = {'customer_id', 'date_order', 'order_line'}
                if forbidden_fields & vals.keys():
                    raise UserError("You cannot modify a confirmed or done sales order.")
        return super(SalesOrder, self).write(vals)
    def unlink(self):
        for order in self:
            if order.state in ('confirmed', 'done'):
                raise UserError("You cannot delete a confirmed or done sales order.")
        return super(SalesOrder, self).unlink()
    @api.constrains('order_line')
    def check_order_line(self):
        for order in self:
            if order.state == 'confirmed' and not order.order_line:
                raise UserError("You cannot confirm a sales order without order lines.")
    @api.onchange('order_line')
    def _onchange_order_line(self):
            if not self.order_line:
                return {
                    'warning': {
                        'title': 'Warning',
                        'message': 'Order has no lines'
                    }
                }
class SalesOrderLine(models.Model):
    _name = "sales.order.line"
    _description = "Sales Order Line"
    order_id = fields.Many2one('sales.order', string='Order')
    product_id = fields.Many2one('product.product', string='Product', required=True)
    quantity = fields.Float(default=1.0, string='Quantity')
    price_unit = fields.Float(digits=(16,2), string='Unit Price', required=True)
    subtotal = fields.Float(compute='_compute_subtotal', store=True, string='Subtotal')
    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit
    @api.constrains('quantity', 'price_unit')
    def check_quantity_and_unit_price(self):
        for line in self:
            if line.quantity <= 0 or line.price_unit <= 0:
                raise UserError("Quantity and Unit Price must be greater than zero.")