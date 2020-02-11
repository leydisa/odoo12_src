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
    state = fields.Selection([('draft', 'Draft')],
                             string='State',
                             default='draft')
