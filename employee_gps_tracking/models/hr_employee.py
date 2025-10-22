from odoo import models, fields, api

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    current_attendance_id = fields.Many2one(
        'hr.attendance',
        compute='_compute_current_attendance',
        string="Current Attendance",
        store=True
    )
    latest_latitude = fields.Float(
        related='current_attendance_id.latest_location_id.latitude',
        string="Latest Latitude",
        readonly=True
    )
    latest_longitude = fields.Float(
        related='current_attendance_id.latest_location_id.longitude',
        string="Latest Longitude",
        readonly=True
    )

    @api.depends('attendance_ids') # This depends on the hr_attendance module's field
    def _compute_current_attendance(self):
        for employee in self:
            employee.current_attendance_id = self.env['hr.attendance'].search([
                ('employee_id', '=', employee.id),
                ('check_out', '=', False)
            ], limit=1)

    def open_live_map(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_url',
            'url': f'https://www.google.com/maps/search/?api=1&query={self.latest_latitude},{self.latest_longitude}',
            'target': 'new',
        }

    @api.model
    def get_live_employee_data(self):
        active_attendances = self.env['hr.attendance'].search([
            ('check_out', '=', False)
        ])
        employee_data = []
        for attendance in active_attendances:
            # Get the most recent location for this specific attendance
            latest_location = self.env['hr.attendance.location'].search([
                ('attendance_id', '=', attendance.id)
            ], order='timestamp desc', limit=1)

            if latest_location:
                employee_data.append({
                    'id': attendance.employee_id.id,
                    'name': attendance.employee_id.name,
                    'latest_latitude': latest_location.latitude,
                    'latest_longitude': latest_location.longitude,
                })
        return employee_data