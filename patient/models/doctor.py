from odoo import models, fields

class HMSDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(string="First Name", required=True)
    last_name = fields.Char(string="Last Name", required=True)
    department_id = fields.Many2one('hms.department', string="Department", domain="[('is_opened', '=', True)]")
    image = fields.Image(string="Image")
    department_capacity = fields.Integer(string="Department Capacity", related='department_id.capacity', readonly=True)
    department_name = fields.Char(string="Department Name", related="department_id.name", store=True)
