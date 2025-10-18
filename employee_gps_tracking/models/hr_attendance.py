from odoo import models, fields, api
from geopy.distance import geodesic

class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    location_ids = fields.One2many(
        comodel_name='hr.attendance.location',
        inverse_name='attendance_id',
        string='GPS Location Points'
    )
    total_distance = fields.Float(
        string='Total Distance (km)',
        compute='_compute_total_distance',
        store=True,
        digits=(10, 2),
        help="Total distance traveled during the attendance period, based on GPS points."
    )
    latest_location_id = fields.Many2one(
        'hr.attendance.location',
        compute='_compute_latest_location',
        string="Latest Location",
        store=True
    )

    @api.depends('location_ids')
    def _compute_latest_location(self):
        for attendance in self:
            if attendance.location_ids:
                attendance.latest_location_id = attendance.location_ids.sorted('timestamp')[-1]
            else:
                attendance.latest_location_id = False

    @api.depends('location_ids')
    def _compute_total_distance(self):
        for attendance in self:
            total_dist = 0.0
            sorted_locations = attendance.location_ids.sorted('timestamp')
            
            if len(sorted_locations) > 1:
                for i in range(len(sorted_locations) - 1):
                    loc1 = sorted_locations[i]
                    loc2 = sorted_locations[i+1]
                    
                    point1 = (loc1.latitude, loc1.longitude)
                    point2 = (loc2.latitude, loc2.longitude)
                    total_dist += geodesic(point1, point2).kilometers

            attendance.total_distance = total_dist
