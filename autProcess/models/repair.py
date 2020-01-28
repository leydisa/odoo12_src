# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class Repair(models.Model):
    """
    Class that represent Repair.
    """
    _description = 'Repair'
    _name = "repair"
    _rec_name = 'code'

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    rma = fields.Char(string='RMA',
                      required=True,
                      default=_('New'))
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    description = fields.Text('Description',
                              required=True)
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)
    cancel_reason = fields.Text('Reason for cancellation')
    state = fields.Selection([('draft', 'Draft'),
                              ('received', 'Received'),
                              ('cancel', 'Cancel')],
                             string='State',
                             default='draft')

    @api.one
    def action_finalized(self):
        """
        Generate the code.
        :return:
        """
        sequence = 'mc.%s.contract.sequence' % ('supplier' if self.supplier else 'customer')
        self.code = self.env['ir.sequence'].next_by_code(sequence)
        return super(Repair, self).action_finalized()