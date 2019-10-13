# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Maintenance Control System',
    'version': '1.0',
    'summary': 'Maintenance Control',
    'description': "Maintenance Control",
    'website': 'https://www.example.com',
    'depends': [],
    'category': 'maintenance_control_system',
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

        'report/report.xml',
        'report/rp_work_order.xml',
        'report/rp_maintenance.xml',
        'report/rp_maintenance_received.xml',
        'report/rp_maintenance_provided.xml',

        'wizard/maintenance_received_wz_view.xml',
        'wizard/maintenance_provided_wz_view.xml',

        'views/mc_nomenclator.xml',
        'views/mc_partner.xml',
        'views/mc_contract.xml',
        'views/mc_material.xml',
        'views/mc_equipement.xml',
        'views/mc_labor.xml',
        'views/mc_work_order.xml',
        'views/mc_maintenance.xml',
        'views/maintenance_control.xml',
    ],
    'qweb': [
    ],
    'test': [
    ],
    'installable': True,
    'application': True,
    'auto_install': True,
}
