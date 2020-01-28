# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'autProcess',
    'version': '1.0',
    'summary': 'autProcess',
    'description': "autProcess",
    'website': 'https://www.example.com',
    'depends': [],
    'category': 'autProcess',
    'sequence': 13,
    'demo': [
    ],
    'depends': [
        'base_setup',
        'resource',
        'web',
    ],
    'data': [
        'data/data.xml',
        'data/sequence.xml',
        'data/paper_format.xml',

        'security/security.xml',
        'security/ir.model.access.csv',

        'views/nomenclator.xml',
        'views/repair.xml',
        'menu.xml',
    ],
    'qweb': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
