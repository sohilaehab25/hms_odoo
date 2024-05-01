from odoo import models, fields


class HMSDepartment(models.Model):
    _name = 'hms.department'
    _description = 'Hospital Department'

    name = fields.Char(required=True)
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    patients = fields.One2many('patient', 'department_id', string="Patients")
    doctors = fields.Many2many('hms.doctor', string="Doctors")
