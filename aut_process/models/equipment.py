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
        ('name_uniq', 'unique (name)',
         'The name must be unique!')
    ]

    @api.model
    def name_search(self, name='', args=None, operator='ilike', limit=100):
        """
        Search by name and series.
        """
        args = args or []
        args += ['|', ('serial', operator, name), ('name', operator, name)]
        print(args)
        recs = self.search(args, limit=limit)
        return recs.name_get()
