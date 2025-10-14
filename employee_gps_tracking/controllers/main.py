from odoo import http
from odoo.http import request, Response
import json

class GpsTrackingController(http.Controller):

    @http.route('/employee_gps_tracking/add_location', type='json', auth='user', methods=['POST'])
    def add_location(self, latitude, longitude, **kwargs):
        # Find the current user's last attendance record that has not been checked out
        attendance = request.env['hr.attendance'].search([
            ('employee_id', '=', request.env.user.employee_id.id),
            ('check_out', '=', False)
        ], limit=1, order='check_in desc')

        if not attendance:
            return {'status': 'error', 'message': 'No active attendance record found.'}

        try:
            request.env['hr.attendance.location'].create({
                'attendance_id': attendance.id,
                'latitude': latitude,
                'longitude': longitude,
            })
            return {'status': 'success', 'message': 'Location recorded'}
        except Exception as e:
            return {'status': 'error', 'message': str(e)}
