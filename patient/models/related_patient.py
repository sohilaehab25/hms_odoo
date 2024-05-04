from odoo import models, fields, api
from odoo.exceptions import ValidationError

class ResPartner(models.Model):
    _inherit = 'res.partner'

    related_patient_id = fields.Many2one('patient', string="Related Patient", help="Related patient for this customer")
    vat = fields.Char(required=True)

    @api.constrains('related_patient_id')
    def _check_unique_patient(self):
        for partner in self:
            if partner.related_patient_id:
                existing_partner = self.env['res.partner'].search([('related_patient_id', '=', partner.related_patient_id.id), ('id', '!=', partner.id)])
                if existing_partner:
                    raise ValidationError("The patient is already assigned to another customer.")
