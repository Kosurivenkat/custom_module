from odoo import fields,api,models

class Customers(models.Model):
    _name="real.customer"
    _description = "Real Estate Customers"

    customer_name=fields.Char("Customer Name")
    email_id=fields.Char("Email Id",required=True)
    phone=fields.Char("Phone Number",required=True)
    selected_customer=fields.Boolean("Selected Customer")
    Address=fields.Char("Address")
    quoted_price=fields.Integer("Quoted Price")
    final_price=fields.Integer("Final Price")
    price_difference=fields.Integer("Price Difference",compute="_compute_price_difference")

    @api.depends("quoted_price","final_price")
    def _compute_price_difference(self):
        for price in self:
            price.price_difference=price.quoted_price-price.final_price






