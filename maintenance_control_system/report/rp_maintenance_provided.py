# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class report_rp_maintenance_provided(models.AbstractModel):
    _name = 'report.maintenance_control_system.rp_maintenance_provided'
    _description = 'Maintenance Provided Report'

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
        if data['form']['partner_id']:
            dom += [('partner_id', '=', data['form']['partner_id'][0])]
        if data['form']['partner1_id']:
            dom += [('partner1_id', '=', data['form']['partner1_id'][0])]
        dom += [('type', '=', data['form']['type'])]
        dom += [('state', '=', 'finalized')]
        docs = self.env['mc.maintenance'].search(dom)
        return {
            'doc_model': 'mc.maintenance',
            'docs': docs,
            'data': dict(
                data,
            ),
        }

