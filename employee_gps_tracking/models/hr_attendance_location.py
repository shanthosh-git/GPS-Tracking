from odoo import models, fields

class HrAttendanceLocation(models.Model):
    _name = 'hr.attendance.location'
    _description = 'HR Attendance Location'

    attendance_id = fields.Many2one(
        comodel_name='hr.attendance',
        string='Attendance Record',
        required=True,
        ondelete='cascade',
        index=True
    )
    latitude = fields.Float(string='Latitude', digits=(10, 7))
    longitude = fields.Float(string='Longitude', digits=(10, 7))
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now, required=True)
    travel_distance = fields.Float(string='distance travelled')
