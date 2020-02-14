# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _


class Repair(models.Model):
    """
    Class representing the equipment of a repair.
    """
    _name = 'repair'
    _rec_name = 'code'
    _description = 'Repair'

    reception_id = fields.Many2one('reception',
                                   ondelete='cascade')
    received_date = fields.Date(related='reception_id.received_date')
    accepted_date = fields.Date(related='reception_id.accepted_date')
    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    equipment_id = fields.Many2one('equipment',
                                   string='Equipment',
                                   required=True)
    type_id = fields.Many2one(related='equipment_id.type_id')
    serial = fields.Char(related='equipment_id.serial')
    symptom_id = \
        fields.Many2one('nomenclator',
                        string='Symptom',
                        domain=[('type_id.code', '=', 'symptom_type')])
    diagnosis_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis',
                        domain=[('type_id.code', '=', 'diagnosis_type')])
    diagnosis_level1_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis',
                        domain=[('type_id.code', '=', 'diagnosis_type')])
    diagnosis_level2_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis',
                        domain=[('type_id.code', '=', 'diagnosis_type')])
    diagnosis_level2_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis',
                        domain=[('type_id.code', '=', 'diagnosis_type')])

    state = fields.Selection([('no_started', 'Draft')],
                             string='',
                             default='draft')
