# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class EmployeeGPS(http.Controller):

    @http.route('/employee_gps_tracking/live_track', type='http', auth='user', website=True)
    def live_track_page(self, **kw):
        return request.render('employee_gps_tracking.live_track_page', {})