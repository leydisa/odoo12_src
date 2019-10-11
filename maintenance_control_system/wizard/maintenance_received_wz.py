# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime

from odoo import api, fields, models


class MaintenanceReceivedWz(models.TransientModel):
    _name = 'maintenance.received.wz'
    _description = 'Maintenance Received Wizard'

    date_from = fields.Date(string='Date From',
                            required=True,
                            default=datetime.now().strftime('%Y-01-01'))
    date_to = fields.Date(string='Date To',
                          required=True,
                          default=datetime.now().strftime('%Y-12-31'))
    entity_id = fields.Many2one('mc.partner',
                                string='Entity',
                                domain=[('supplier', '=', False),
                                        ('type', '=', 'internal')])
    supplier_id = fields.Many2one('mc.partner',
                                  string='Proveedor',
                                  domain=[('supplier', '=', True)])

    @api.multi
    def print_report(self):
        datas = {'form': self.read(['date_from', 'date_to', 'entity_id', 'supplier_id'])[0]}
        return self.env.ref('maintenance_control_system.report_maintenance_received_id').report_action([], data=datas)
