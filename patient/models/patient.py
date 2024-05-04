from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import date
import re


class Patient(models.Model):
    _name = 'patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    age = fields.Integer(compute='_compute_age', store=True)
    email = fields.Char(string="Email", required=True, unique=True)
    blood_type = fields.Selection([
        ('O-', 'O-'),
        ('O+', 'O+'),
        ('AB', 'AB'),
        ('A-', 'A-'),
        ('A+', 'A+'),
        ('B+', 'B+'),
        ('B-', 'B-')
    ])
    address = fields.Text()
    image = fields.Image()
    history = fields.Html(attrs={'invisible': [('age', '&lt;', 50)]})
    CR_ratio = fields.Float()
    pcr = fields.Boolean(string='PCR')
    department_id = fields.Many2one('hms.department', string="Department", domain="[('is_opened', '=', True)]")
    department_capacity = fields.Integer(related='department_id.capacity', string="Department Capacity")
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors", domain="[('department_id', '=', department_id)]")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined', string='State')
    log_ids = fields.One2many('patient.log', 'patient_id', string='Log History')

    @api.onchange('age')
    def onchange_age(self):
        if self.age < 30:
            self.pcr = True
            return {
                'warning': {
                    'title': "PCR Checked",
                    'message': "PCR has been automatically checked because age is lower than 30."
                }
            }

    @api.constrains('email')
    def _check_unique_email(self):
        for record in self:
            if record.email:
                # Check for basic email format (www@domain.extension)
                if not re.match(r"^[^@]+@[^@]+\.[a-zA-Z]{2,}$", record.email):
                    raise ValidationError("Invalid email format. Please enter a valid email address like 'user@example.com'.")

                # Existing unique email check (unchanged)
                existing_patient = self.env['patient'].search([('email', '=', record.email), ('id', '!=', record.id)])
                if existing_patient:
                    raise ValidationError("Email address must be unique. The email '{}' is already used by another patient.".format(record.email))

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 1

    def write(self, vals):
        if 'state' in vals:
            description = f"State changed to {vals['state']}"
            for patient in self:
                patient.log_ids.create({
                    'patient_id': patient.id,
                    'description': description
                })
        return super(Patient, self).write(vals)
