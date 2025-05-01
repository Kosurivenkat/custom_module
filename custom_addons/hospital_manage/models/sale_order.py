from odoo import models, fields

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    marketing_user = fields.Many2one('res.users', string='Marketing User')
