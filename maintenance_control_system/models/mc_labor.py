# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import fields, models, api


class McLabor(models.Model):
    """
    Class that represent Labor.
    """
    _description = 'Labor Costs'
    _name = "mc.labor"
    _rec_name = "date"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    @api.one
    @api.depends('maintenance_ids')
    def _compute_used(self):
        """
        Calculate the current coste of the material.
        :return:
        """
        self.used = self.env['mc.maintenance'].search([('labor_id', '=', self.id)], limit=1) == 1

    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    coste_cuc = fields.Float(string='CUC',
                             required=True)
    coste_cup = fields.Float(string='CUP',
                             required=True)
    used = fields.Boolean(compute=_compute_used,
                          store=True)
    maintenance_ids = fields.One2many('mc.maintenance', 'labor_id')

    _sql_constraints = [
        ('coste_zero', 'CHECK (coste_cuc > 0 or coste_cup > 0)', 'The coste must be greater than 0.'),
        ('date_unique', 'unique (date)', 'Repeated date!'),
    ]

