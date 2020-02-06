# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class Equipment(models.Model):
    """
    Class representing a equipment.
    """
    _name = 'equipment'
    _rec_name = 'serial'
    _description = 'Equipment'

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    serial = fields.Char(string='Serial Number',
                         required=True)
    date = fields.Date(string='Creation Date',
                       readonly=True,
                       default=_get_default_date)
    type_id = fields.Many2one('nomenclator',
                              string='Type',
                              required=True,
                              domain=[('type_id.code', '=', 'equipment_type')])
    description = fields.Char('Description',
                              required=True)

    _sql_constraints = [
        ('serial_uniq', 'unique (serial)',
         'The serial must be unique!'),
        ('description__uniq', 'unique (description)',
         'The description must be unique!')
    ]
