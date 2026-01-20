from  odoo import models, fields
class SaleOrderChangeStateToReject(models.TransientModel):
    _name = 'sale.order.reject'
    sale_order_id = fields.Many2one('sale.order', string='Sale Order', required=True)
    reject_reason = fields.Char(string='Reject Reason', required=True)
    def action_confirm_reject(self):
        self.sale_order_id.write(
            {
                'state': 'reject',
                'rejection_reason': self.reject_reason,
                'rejection_by': self.env.user.name,
                'rejection_date': fields.Datetime.now()
                                  }
        )
