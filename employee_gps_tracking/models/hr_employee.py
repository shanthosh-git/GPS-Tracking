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
        clocked_in_employees = self.env['hr.employee'].search([
            ('current_attendance_id', '!=', False),
            ('latest_latitude', '!=', 0),
            ('latest_longitude', '!=', 0),
        ])
        return clocked_in_employees.read([
            'id',
            'name',
            'latest_latitude',
            'latest_longitude',
        ])