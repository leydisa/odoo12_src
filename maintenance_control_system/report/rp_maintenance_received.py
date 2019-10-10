# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models
from odoo.tools import float_round


class report_rp_maintenance_received(models.AbstractModel):
    _name = 'report.maintenance_control_system.rp_maintenance_received'
    _description = 'Maintenance Received Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        """

        :param docids:
        :param data:
        :return:
        """
        data = data if data is not None else {}
        dom = [('datetime_start', '>=', data['form']['date_from'])]
        dom += [('datetime_start', '<=', data['form']['date_to'])]
        if data['form']['entity_id']:
            dom += [('partner_id', '<=', data['form']['entity_id'][0])]
        if data['form']['supplier_id']:
            dom += [('partner_id', '<=', data['form']['supplier_id'][0])]
        dom += [('type', '=', 'mr')]
        dom += [('state', '=', 'finalized')]
        docs = self.env['mc.maintenance'].search(dom)
        return {
            'doc_model': 'mc.maintenance',
            'docs': docs,
            'data': dict(
                data,
            ),
        }

