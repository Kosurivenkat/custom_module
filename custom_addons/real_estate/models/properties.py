from odoo import api,fields,models
class Properties(models.Model):
    _name="real.properties"
    _description="Real estate"

    property_name=fields.Char("Property name",required=True)
    price=fields.Integer("Price",required=True)
    location=fields.Char("Location",required=True)
    company_mail=fields.Char("Company Mail",required=True)
    all_properties=fields.Many2many("customers")
    state=fields.Char("State")
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('negotiation', 'Negotiation'),
        ('confirmed', 'Confirmed'),
        ('closed', 'Closed')
    ], string="Stage", default='draft', tracking=True)


    def action_set_draft(self):
        self.stage = 'draft'

    def action_set_negotiation(self):
        self.stage = 'negotiation'

    def action_set_confirmed(self):
        self.stage = 'confirmed'

    def action_set_closed(self):
        self.stage = 'closed'

    def action_open_send_mail_wizard(self):
        self.ensure_one()
        cust_id = ', '.join(email for email in self.all_properties.mapped('company_mail') if email)
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_company_mail': self.company_mail,
                'default_customer_mail': cust_id,
            },
        }








