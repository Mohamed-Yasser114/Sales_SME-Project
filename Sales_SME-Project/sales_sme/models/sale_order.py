from  odoo import api, fields, models
class SaleOrder(models.Model):
    _inherit = 'sale.order'
    state = fields.Selection(selection_add=[('reject', 'Reject')])
    rejection_by = fields.Char(string='Rejection By', readonly=True)
    rejection_reason = fields.Char(string='Rejection Reason', readonly=True)
    rejection_date = fields.Datetime(string='Rejection Date', readonly=True)
    contact_ids = fields.One2many('res.partner', inverse_name='parent_id', string='Contact Info', readonly=True)
    flag = fields.Boolean(string='Flag')
    def action_open_reject_wizard(self):
        self.ensure_one()
        return {
            'name': 'Reject',
            'type': 'ir.actions.act_window',
            'res_model': 'sale.order.reject',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_sale_order_id': self.id},
        }
    @api.onchange('partner_id')
    def Change_Contact_Info(self):
        for order in self:
            if order.partner_id:
                self.contact_ids = self.partner_id.child_ids
