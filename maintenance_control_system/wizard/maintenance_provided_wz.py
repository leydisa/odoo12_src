# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models


class MaintenanceProvidedWz(models.TransientModel):
    _name = 'maintenance.provided.wz'
    _description = 'Maintenance Provided Wizard'

    date_from = fields.Date(string='Date From',
                            required=True,
                            default=datetime.now().strftime('%Y-01-01'))
    date_to = fields.Date(string='Date To',
                          required=True,
                          default=datetime.now().strftime('%Y-12-31'))
    partner_id = fields.Many2one('mc.partner')
    partner1_id = fields.Many2one('mc.partner')
    type = fields.Char(default=lambda self: self.env.context.get('type') or False)

    @api.multi
    def print_report(self):
        datas = {'form': self.read(['date_from', 'date_to', 'partner_id', 'partner1_id', 'type'])[0]}
        return self.env.ref('maintenance_control_system.report_maintenance_provided_id').report_action([], data=datas)
