from odoo import models, fields, api
from odoo.exceptions import UserError

class RealEstateMailWizard(models.TransientModel):
    _name = "real.mail.wizard"
    _description = "Send mail to customers"

    company_mail=fields.Char("Company mail")
    comp_id=fields.Many2many("real.properties")
    cust_id=fields.Many2many("real.customer")
    customer_mail=fields.Char("Customer mail")
    comment=fields.Text("Comment")


    def action_send_mail(self):
        if not self.cust_id:
            raise UserError("No customer is selected.")

        email_to = self.company_mail
        email_cc = ','.join([doc.email for doc in self.cust_id if doc.email])

        email_body = f"""
              <p>Dear {self.comp_id.name},</p>
              <p>{self.comment}</p>
              <p>Best regards,<br/>Hospital Management</p>
          """

        mail_values = {
            'subject': f"Property Report - {self.comp_id.name}",
            'email_from': self.env.user.email or 'admin@example.com',
            'email_to': email_to,
            'email_cc': email_cc,
            'body_html': email_body,
            'state': 'outgoing',
        }

        self.env['mail.mail'].create(mail_values).send()
        self.comp_id.stage = 'confirmed'

        return {'type': 'ir.actions.act_window_close'}