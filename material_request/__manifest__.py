# -*- coding: utf-8 -*-

{
    'name': "Material Request",
    'depends': ['base', 'hr', 'stock', 'purchase'],
    'version': '16.0.1.0.0',
    'author': 'Ashvad',
    'description': "material request",
    'category': 'material/request',

    'data': [
        'data/ir_sequence.xml',
        'security/security_groups.xml',
        'security/ir.model.access.csv',
        'views/material_request.xml',
        'views/material_menus.xml'
    ],

    'license': 'LGPL-3',

    'installable': True,
    'application': True,
    'auto_install': False
}
