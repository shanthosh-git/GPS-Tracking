{
    'name': 'Employee GPS Location Tracking',
    'version': '1.0',
    'summary': 'Track employee location during attendance and calculate distance traveled.',
    'category': 'Human Resources/Attendances',
    'author': 'Gemini',
    'depends': ['hr_attendance'],
    'data': [
        'security/ir.model.access.csv',
        'views/hr_attendance_views.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
