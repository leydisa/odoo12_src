# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Repair(models.Model):
    """
    Class representing the equipment of a repair.
    """
    _name = 'repair'
    _inherit = 'notification'
    _rec_name = 'code'
    _description = 'Repair'

    reception_id = fields.Many2one('reception',
                                   readonly=True,
                                   ondelete='cascade')
    accepted_date = fields.Date(related='reception_id.accepted_date')
    accepted_by = fields.Many2one(related='reception_id.accepted_by')
    code = fields.Char(string='Code',
                       readonly=True)
    repair_date = fields.Date('Repair Date',
                              readonly=True)
    repair_by = fields.Many2one('res.users',
                                string='Repair By',
                                readonly=True)
    equipment_id = fields.Many2one('equipment',
                                   string='Equipment',
                                   required=True)
    equipment_type_id = fields.Many2one(related='equipment_id.type_id')
    serial = fields.Char(related='equipment_id.serial')
    symptom_id = \
        fields.Many2one('nomenclator',
                        string='Symptom',
                        domain=[('type_id.code', '=', 'symptom_type')])
    diagnosis_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis',
                        domain=[('type_id.code', '=', 'diagnosis_type')])
    diagnosis_level1_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis Level 1',
                        domain=[('type_id.code', '=', 'diagnosis_type')])
    diagnosis_level2_id = \
        fields.Many2one('nomenclator',
                        string='Diagnosis Level 2',
                        domain=[('type_id.code', '=', 'diagnosis_type')])
    repair_type = fields.Selection([('A', 'A: Mild Entity (new tests, replacement of worn out external parts, battery recharge, etc.)'),
                                    ('B', 'B: Medium Entity (electronic card replacement)'),
                                    ('C', 'C: Serious Entity (device replacement)')],
                                   string='Repair Type')
    notification_ids = fields.One2many('mail.message', 'res_id',
                                       string='Notifications',
                                       domain=[('model', '=', 'repair')])
    state = fields.Selection([('not_started', 'Not Started'),
                              ('in_process', 'In Process'),
                              ('finished', 'Finished')],
                             string='State',
                             default='not_started')

    @api.one
    def action_in_process(self):
        """
        Set to state in_process.
        :return:
        """
        self.state = 'in_process'

    @api.one
    def action_finished(self):
        """
        Set to state finished.
        :return:
        """
        self.repair_by = self.env.user.id
        self.repair_date = datetime.today().strftime(DEFAULT_SERVER_DATE_FORMAT)
        self._send_notification('email_template_second_customer_notification')
        self._send_notification('email_template_contact_request_form')
        self.state = 'finished'
