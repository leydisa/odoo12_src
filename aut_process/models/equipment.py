# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class Equipment(models.Model):
    """
    Class representing a equipment.
    """
    _name = 'equipment'
    _description = 'Equipment'

    name = fields.Char('Name',
                       required=True)
    serial = fields.Char(string='Serial Number',
                         required=True)
    type_id = fields.Many2one('nomenclator',
                              string='Type',
                              required=True,
                              domain=[('type_id.code', '=', 'equipment_type')])
    date = fields.Date(string='Creation Date',
                       readonly=True,
                       default=fields.Date.today)

    _sql_constraints = [
        ('serial_uniq', 'unique (serial)',
         'The serial must be unique!'),
        ('description__uniq', 'unique (description)',
         'The description must be unique!')
    ]
