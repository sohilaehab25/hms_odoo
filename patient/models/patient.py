from odoo import models, fields, api


class Patient(models.Model):
    _name = 'patient'
    _description = 'Hospital Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    birth_date = fields.Date()
    age = fields.Integer()
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
    doctor_ids = fields.Many2many('hms.doctor', string="Doctors", readonly=True, domain="[('department_id', '=', department_id)]")
    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined', string='State')
    log = fields.Text()

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
