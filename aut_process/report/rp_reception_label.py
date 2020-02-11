# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, models


class report_rp_reception_label(models.AbstractModel):
    _name = 'report.aut_process.rp_reception_label'
    _description = 'Reception Label'

    @api.model
    def _get_report_values(self, docids, data=None):
        """

        :param docids:
        :param data:
        :return:
        """
        docs = self.env['reception'].browse(docids)
        return {
            'doc_model': 'reception',
            'docs': docs,
            'data': dict(
                data,
            ),
        }