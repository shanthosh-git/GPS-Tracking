# -*- coding: utf-8 -*-
import logging
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)

class EmployeeGPS(http.Controller):

    @http.route('/employee_gps_tracking/add_location', type='json', auth='user')
    def add_location(self, latitude, longitude):
        _logger.info(f"Received location data: lat={latitude}, lng={longitude} for user: {request.env.user.name}")
        employee = request.env.user.employee_id
        if not employee:
            _logger.warning(f"No employee found for user: {request.env.user.name}")
            return {'status': 'failed', 'reason': 'No employee linked to user'}

        _logger.info(f"Found employee: {employee.name}")
        attendance = request.env['hr.attendance'].search([
            ('employee_id', '=', employee.id),
            ('check_out', '=', False)
        ], limit=1)

        if not attendance:
            _logger.warning(f"No active attendance record found for employee: {employee.name}")
            return {'status': 'failed', 'reason': 'No active attendance'}

        _logger.info(f"Found active attendance {attendance.id} for employee: {employee.name}")
        location = request.env['hr.attendance.location'].create({
            'attendance_id': attendance.id,
            'latitude': latitude,
            'longitude': longitude,
        })
        _logger.info(f"Successfully created location record {location.id} for attendance {attendance.id}")
        return {'status': 'success'}

    @http.route('/employee_gps_tracking/live_track', type='http', auth='user', website=True)
    def live_track_page(self, **kw):
        return request.render('employee_gps_tracking.live_track_page', {})