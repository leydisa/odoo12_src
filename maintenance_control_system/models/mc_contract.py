# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class McContract(models.Model):
    """
    Class that represent Contracts.
    """
    _description = 'Contract'
    _inherit = ['doc.state']
    _name = "mc.contract"
    _rec_name = 'code'

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    @api.constrains('date', 'expiration_date')
    def _check_data(self):
        """
        It is checked that the start date / time is less than the final date.
        :return:
        """
        if self.expiration_date and \
                not (fields.Datetime.from_string(self.expiration_date) > fields.Datetime.from_string(self.date)):
            raise ValidationError(_('The start date must be less than the expiration date.'))

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    description = fields.Text('Description',
                              required=True)
    expiration_date = fields.Date(string='Expiration Date')
    expiration_date_editable = fields.Boolean(default=True)
    file = fields.Binary(string="Document",
                         required=True)
    filename = fields.Char('File Name',
                           required=True)
    partner_id = fields.Many2one('mc.partner',
                                 required=True,
                                 ondelete='restrict')
    supplier = fields.Boolean(string='Is a Vendor',
                              default=lambda self: self.env.context.get('supplier') or False)
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)

    @api.multi
    def write(self, vals):
        """
        Edit the end date until one is set.
        :param values:
        :return:
        """
        if 'expiration_date' in vals:
            vals['expiration_date_editable'] = False
        return super(McContract, self).write(vals)

    @api.multi
    def unlink(self):
        """
        It is not possible to delete in the finalized state.
        :return:
        """
        if self.state == 'finalized':
            raise ValidationError('It is not possible to delete in the finalized state.')
        return super(McContract, self).unlink()

    @api.one
    def action_finalized(self):
        """
        Generate the code.
        :return:
        """
        sequence = 'mc.%s.contract.sequence' % ('supplier' if self.supplier else 'customer')
        self.code = self.env['ir.sequence'].next_by_code(sequence)
        return super(McContract, self).action_finalized()