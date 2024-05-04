from odoo import models, fields, api

class PatientLog(models.Model):
    _name = 'patient.log'
    _description = 'Patient Log'

    patient_id = fields.Many2one('patient', string='Patient', required=True, ondelete='cascade')
    created_by = fields.Many2one('res.users', string='Created by', default=lambda self: self.env.user)
    date = fields.Datetime(default=lambda self: fields.datetime.now())
    description = fields.Text()
    
    
    