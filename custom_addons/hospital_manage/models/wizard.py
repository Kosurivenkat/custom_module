from odoo import models, fields, api
from odoo.exceptions import UserError

class HospitalMailWizard(models.TransientModel):
    _name = "hospital.mail.wizard"
    _description = "Send Email to Patient and Doctor"

    patient_id = fields.Many2one('hospital.patient', string="Patient", required=True, readonly=True)
    patient_email = fields.Char(string="Patient Email", required=True, readonly=True)
    doctor_ids = fields.Many2many('hospital.doctors', string="Doctors", readonly=True)
    selected_doctor_email = fields.Char(string="Doctor Emails", required=True,readonly=True)
    message = fields.Text(string="Message", required=True)

    @api.model
    def default_get(self, fields_list):
        defaults = super().default_get(fields_list)
        patient_id = self.env.context.get('default_patient_id')

        if patient_id:
            patient = self.env['hospital.patient'].browse(patient_id)
            defaults['patient_email'] = patient.email
            defaults['doctor_ids'] = [(6, 0, selected_doctors.ids)]
            defaults['selected_doctor_email'] = ', '.join([doc.email for doc in selected_doctors if doc.email])

        return defaults

    def action_send_mail(self):
        if not self.doctor_ids:
            raise UserError("No doctors selected for this patient.")

        email_body = f"""
            <p>Dear {self.patient_id.name},</p>
            <p>{self.message}</p>
            <p>Best regards,<br/>Hospital Management</p>
        """

        mail_values = {
            'subject': f"Patient Report - {self.patient_id.name}",
            'email_from': self.env.user.email or 'admin@example.com',
            'body_html': email_body,
            'state': 'outgoing',
        }

        mail = self.env['mail.mail'].create(mail_values)
        mail.send()


        return {'type': 'ir.actions.act_window_close'}
