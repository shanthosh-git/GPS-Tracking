{
    'name': 'Employee GPS Location Tracking',
    'version': '1.0',
    'summary': 'Track employee location during attendance and calculate distance traveled.',
    'category': 'Human Resources/Attendances',
    'author': 'Gemini',
    'depends': ['hr_attendance', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_views.xml',
        'views/hr_employee_views.xml',
        'views/employee_gps_tracking_views.xml',
    ],
    'assets': {
    'web.assets_backend': [
        'employee_gps_tracking/static/src/js/map.js',
        'employee_gps_tracking/static/src/xml/map_template.xml',
        'https://maps.googleapis.com/maps/api/js?key=AIzaSyAOBCkcBNfaHnfEqt1wm26MQeeVqhejN7E',
    ],
},

    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
