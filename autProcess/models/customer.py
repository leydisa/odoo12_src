# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class Customer(models.Model):
    """
    Class that represent Equipment.
    """
    _name = "customer"
    _rec_name = 'name'
    _description = 'Customer'

    name = fields.Char('Name',
                       required=True)
    address = fields.Char('Address',
                          required=True)
    email = fields.Char('Email',
                        required=True)
    phone = fields.Char('Phone',
                        required=True)
    at_hw = fields.Boolean('Contrato de AT HW')
    at_sw = fields.Boolean('Contrato de AT SW')
    sla = fields.Float('SLA (hours)',
                         required=True)

    _sql_constraints = [
        ('name_uniq', 'unique (name)',
         'The name must be unique!'),
        ('check_sla', 'CHECK(sla > 0)',
         'SLA must be greater than 0!')
    ]
