from odoo import models, fields, api


class HospitalActiveDoctorsWizard(models.TransientModel):
    _name = 'hospital.active.doctors.wizard'
    _description = 'Selected Active Doctors Wizard'

    doctor_ids = fields.One2many('hospital.active.doctors.line', 'wizard_id')

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_patient_id = self.env.context.get('active_id')
        patient = self.env['hospital.patient'].browse(active_patient_id)
        doctor_lines = []
        for doctor in patient.all_doctors.filtered(lambda d: d.is_selected):
            doctor_lines.append((0, 0, {
                'name': doctor.name,
                'specialty': doctor.specialty,
                'availability_status': doctor.availability_status,
                'treatment_start_date': doctor.treatment_start_date,
                'treatment_end_date': doctor.treatment_end_date,
                'days': doctor.days,
            }))
        res['doctor_ids'] = doctor_lines
        return res


class HospitalActiveDoctorsLine(models.TransientModel):
    _name = 'hospital.active.doctors.line'
    _description = 'Doctor Detail Line'

    wizard_id = fields.Many2one('hospital.active.doctors.wizard', required=True, ondelete='cascade')
    name = fields.Char("Doctor Name")
    specialty = fields.Char("Specialty")
    availability_status = fields.Selection([
        ('available', 'Available'),
        ('busy', 'Busy'),
        ('on_leave', 'On Leave')
    ])
    treatment_start_date = fields.Date()
    treatment_end_date = fields.Date()
    days = fields.Integer("Days")
