from odoo import models, fields

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    location_ids = fields.One2many(
        comodel_name='hr.attendance.location',
        inverse_name='attendance_id',
        string='GPS Location Points'
    )
