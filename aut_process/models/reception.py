# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from .common import FIRST_CUSTOMER_NOTIFICATION


class Reception(models.Model):
    """
    Class representing a reception.
    """
    _name = 'reception'
    _rec_name = 'code'
    _description = 'Reception'

    @api.multi
    @api.constrains('attachment_ids')
    def _check_data(self):
        """
        Check that the minimum number of photos of the open package is 3.
        :return:
        """
        if len(self.attachment_ids) < 3:
            raise ValidationError(_('At least 3 photos of the open package.'))

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       readonly=True,
                       index=True,
                       default=fields.Date.today)
    date_accept = fields.Date('Acceptance Date')
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)
    user_accept_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)
    photo1 = fields.Binary("Photo 1")
    photo2 = fields.Binary("Photo 2")
    photo3 = fields.Binary("Photo 3")
    photo4 = fields.Binary("Photo 4")
    photo5 = fields.Binary("Photo 5")
    ddt_ids = fields.One2many('reception.ddt', 'reception_id',
                              string='DDT')
    attachment_ids = \
        fields.Many2many('ir.attachment',
                         'reception_attachments_rel',
                         'reception_id', 'attachment_id',
                         string='Photographs of the open package',
                         required=True,
                         help='The photographs of the open package vary '
                              'according to the quantity of pieces contained '
                              'in the package (minimum 3 photos), however, '
                              'one photo is taken from above without removing '
                              'anything from the package, while the others '
                              'are taken by placing the entire contents of '
                              'the package at the top a table and taking a '
                              'picture of the objects from the top anyway. '
                              'At the discretion of the operator, photos '
                              'are taken that show details of the equipment '
                              'that may be relevant for the repair. '
                              'The photos are saved and loaded in the relative '
                              'technical file.')
    customer_id = fields.Many2one('customer',
                                  string='Customer')
    repair_ids = fields.One2many('repair', 'reception_id',
                                 string='Equipos')
    contact_inf_name = fields.Char('Name')
    contact_inf_email = fields.Char('Email')
    contact_inf_address = fields.Char('Address')
    state = fields.Selection([('started', 'Started'),
                              ('received', 'Received'),
                              ('in_acceptance', 'In Acceptance'),
                              ('accepted', 'Accepted')],
                             string='State',
                             default='started')

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The code must be unique!')
    ]

    @api.multi
    def write(self, vals):
        """

        :param vals:
        :return:
        """
        tools.image_resize_images(vals)
        return super(Reception, self).write(vals)

    @api.multi
    def unlink(self):
        """
        It is only allowed to delete in the started state.
        :return:
        """
        if self.state != 'started':
            raise ValidationError("It is only allowed to delete in the started "
                                  "state.")
        return super(Reception, self).unlink()

    @api.one
    def action_received(self):
        """
        Generate the RMA code.
        Set to state received.
        :return:
        """
        self.code = self.env['ir.sequence'].next_by_code('reception.sequence')
        self.state = 'received'

    @api.one
    def action_in_acceptance(self):
        """
        Set to state in_acceptance.
        :return:
        """
        self.state = 'in_acceptance'

    @api.one
    def action_accepted(self):
        """
        Set to state accepted.
        :return:
        """
        self.state = 'accepted'

    def print_label(self):
        """
        Imprime las etiqueta.
        :return:
        """
        self.ensure_one()
        return self.env.ref('aut_process.report_repair_label_id'). \
            report_action(None, data={})

    @api.multi
    def send_first_notification(self):
        """
        :return:
        """
        self.ensure_one()
        mails = self.env['mail.mail']
        mail_values = {
            'email_from': 'leydisa@gmail.com',
            'email_to': 'leydisa@gmail.com',
            'subject': 'First Customer Notification',
            'body_html': FIRST_CUSTOMER_NOTIFICATION,
            'notification': True,
            'mailing_id': self.id}
        mail = self.env['mail.mail'].create(mail_values)
        mails |= mail
        mails.send()
        return True


class ReceptionDDT(models.Model):
    """
    Class representing a reception.
    """
    _name = 'reception.ddt'
    _description = 'DDTs'

    reception_id = fields.Many2one('reception',
                                   ondelete='cascade')
    ddt = fields.Binary('DDT',
                        required=True)
    date = fields.Date(string='Date',
                       readonly=True,
                       index=True,
                       default=fields.Date.today)
    verified = fields.Selection([('match', 'Match'),
                               ('dont_match', "Don't Match")],
                              string='Verified?',
                              required=True)
