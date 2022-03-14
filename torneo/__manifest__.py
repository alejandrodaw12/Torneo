# -*- coding: utf-8 -*-
{
    'name': "torneo",

    'summary': """
        Se trata de sesiones de libre participación en las que se inicia una modalidad deportiva. 
        Actividades de competición modificadas o de participación: 
        Son de libre participación, sin selección y tienen por objetivo la mejora de la modalidad deportiva""",

    'description': """
        Long description of module's purpose
    """,

    'author': "Aitor Menta",
    'website': "http://infsalinas.sytes.net:10150/",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','horario'],

    # always loaded
    'data': [
        'security/torneo_security.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        'report/torneo_idCompetidores_report.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'application' : True ,
}
