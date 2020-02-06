# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class report_rp_repair_label(models.AbstractModel):
    _name = 'report.aut_process.rp_repair_label'
    _description = 'Repair Label'

    @api.model
    def _get_report_values(self, docids, data=None):
        """

        :param docids:
        :param data:
        :return:
        """
        docs = self.env['repair'].browse(docids)
        return {
            'doc_model': 'repair',
            'docs': docs,
            'data': dict(
                data,
            ),
        }