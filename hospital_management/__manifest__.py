# -*- coding: utf-8 -*-

{
    'name': "Hospital Management",
    'version': '16.0.1.0.0',
    'depends': ['base', 'contacts', 'mail', 'hr', 'account_payment', 'sale','purchase'],
    'author': 'Ashvad',
    'description': "hospital management is used to effectively manage and co-ordinate resources of a medical organization",
    'maintainer': "Ashvad",

    'category': 'hospital/management',

    'data': [
        'security/security_groups.xml',
        'security/ir.model.access.csv',

        'report/patient_report_template.xml',
        'report/patient_report.xml',

        'data/ir_cron.xml',
        'data/ir_sequence.xml',

        'wizard/patient_report.xml',

        'views/patient_card_views.xml',
        'views/res_partner.xml',
        'views/patient_op_views.xml',
        'views/patient_consultation_views.xml',
        'views/hr_employee.xml',
        'views/patient_appointment_views.xml',

        'views/hospital_menus.xml',

    ],
    'assets' : {
        'web.assets_backend':[
        'hospital_management/static/src/js/action_manager.js'
        ]
    },

    'license': 'LGPL-3',

    'installable': True,

    'application': True,

    'auto_install': False
}
