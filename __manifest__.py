# -*- coding: utf-8 -*-
{
    'name': "Estudiantes",

    'summary': "Registro de estudiantes por servicio adquirido (curso, diplomado, etc.)",

    'description': """

    """,

    'author': "Juan Salvador",
    # 'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Human Resources',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'stock','account'],

    # always loaded
    'data': [
        'data/sequence.xml',       
        'views/curso_detalle_view.xml',
        'views/curso_view.xml',
        'views/alumno_view.xml',
        'views/inscripcion_view.xml',
        'views/generar_curso_view.xml',
        'views/generar_estudiante_view.xml',
        'views/menu_view.xml',
        'security/security.xml',
        'security/ir.model.access.csv',
        'security/ir.rule.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3'
}

