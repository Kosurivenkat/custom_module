import re
# from typing import io

# from reportlab.lib.pagesizes import letter
# from reportlab.pdfgen import canvas

from odoo import api,models, fields
from odoo.exceptions import ValidationError

class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _description = 'Patient Master'

    name=fields.Char('Patient Name',required=True)
    age=fields.Integer('Age',store=True,required=True)
    email=fields.Char('Email',required=True)
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], string="Gender", default='male', required=True)
    phone=fields.Char('Phone',required=True)
    doctor_Id = fields.One2many('hospital.doctors',"patients",string="Doctor", required=False)
    document = fields.Binary('Upload Document')
    patient_status=fields.Selection([('active','Active'),('not_active','Not Active')],string="Patient Status")
    days=fields.Integer('Days')
    all_doctors = fields.Many2many('hospital.doctors', string="Available Doctors")
    doctor_selected = fields.Boolean("Doctor Selected", compute="_compute_doctor_selected", store=True)
    stage = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('to_approve', 'To Approve'),
        ('approved', 'Approved'),
        ('closed', 'Closed')
    ], string="Stage", default='draft', tracking=True)
    patient_id = fields.Char(string="Patient ID", readonly=True, copy=False, default='New')

    @api.depends('doctor_Id')
    def _compute_doctor_selected(self):
        for record in self:
            record.doctor_selected = bool(record.doctor_Id)


    @api.constrains('email')
    def _check_email(self):
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Invalid email format! Please enter a valid email address.")

    @api.constrains('phone')
    def _check_phone(self):
        phone_regex = r'^\+?\d{10,15}$'
        for record in self:
            if record.phone and not re.match(phone_regex, record.phone):
                raise ValidationError("Invalid phone number! It should contain only numbers and be between 10-15 digits.")

    def action_set_draft(self):
        self.stage = 'draft'

    def action_set_active(self):
        self.stage = 'active'

    def action_set_to_approve(self):
        self.stage = 'to_approve'

    def action_set_approved(self):
        self.stage = 'approved'

    def action_set_closed(self):
        self.stage = 'closed'
    def action_print_patient_report(self):
        return self.env.ref('hospital_manage.report_hospital_patient').report_action(self)

    # selected_doctors = fields.Many2many('hospital.doctors', string="Select Doctors")
    def action_open_send_mail_wizard(self):
        self.ensure_one()

        # Ensure we only include doctors with valid email addresses
        doctor_emails = ', '.join(email for email in self.all_doctors.mapped('email') if email)

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hospital.mail.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_patient_email': self.email,
                'default_doctor_ids': self.all_doctors.ids,
                'default_selected_doctor_email': doctor_emails,
            },
        }

    @api.model
    def create(self, vals):
        if vals.get('patient_id', 'New') == 'New':
            vals['patient_id'] = self.env['ir.sequence'].next_by_code('hospital.patient') or 'New'
        return super(HospitalPatient, self).create(vals)









