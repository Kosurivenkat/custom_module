import re

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HospitalDoctors(models.Model):
    _name = 'hospital.doctors'
    _description = 'Doctors'

    name=fields.Char(string="Doctor Name",required=True)
    specialty = fields.Char(string='Specialty')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email',required=True)
    active = fields.Boolean(string='Active', default=True)
    is_selected = fields.Boolean(string="Select Doctor")

    availability_status = fields.Selection([
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('on_leave', 'On Leave')
    ], string='Availability', default='available')
    patients = fields.Many2one("hospital.patient",string='Patients')
    # patients_Id=fields.Many2many('hospital.patient', string='Patients')
    treatment_start_date = fields.Date('Treatment Start Date')
    treatment_end_date = fields.Date('Treatment End Date')
    patient_status = fields.Selection([
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ], string="Patient Status", default='inactive', required=True)

    # Days Field (Visible only if the patient is "Active")
    days = fields.Integer('Days', compute="_compute_days", store=True)

    @api.depends('treatment_start_date', 'treatment_end_date')
    def _compute_days(self):
        """Compute days only if the patient is 'Active'."""
        for record in self:
            if record.treatment_start_date and record.treatment_end_date:
                record.days = (record.treatment_end_date - record.treatment_start_date).days
            else:
                record.days = 0
    @api.constrains('email')
    def _check_email(self):
        """Validate email format"""
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        for record in self:
            if record.email and not re.match(email_regex, record.email):
                raise ValidationError("Invalid email format! Please enter a valid email address.")


