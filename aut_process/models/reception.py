# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

from datetime import datetime
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT


class Reception(models.Model):
    """
    Class representing a reception.
    """
    _name = 'reception'
    _rec_name = 'code'
    _description = 'Reception'

    def _send_first_notification(self):
        """
        Send the first notification to the customer.
        :return:
        """
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('aut_process', 'email_template_reception_first_customer_notification')[1]
        except ValueError:
            template_id = False
        self.env['mail.template'].browse(template_id).send_mail(self.id,
                                                                force_send=True)
        return True

    @api.multi
    @api.constrains('repair_ids')
    def _check_data(self):
        """
        Check that the minimum number of photos of the open package is 3.
        :return:
        """
        if len(self.repair_ids) == 0:
            raise ValidationError(_('Required.'))

    code = fields.Char(string='Code',
                       required=True,
                       readonly=True,
                       default=_('New'))
    received_date = fields.Date(string='Received Date',
                                readonly=True)
    received_by = fields.Many2one('res.users',
                                  string='Received By',
                                  readonly=True)
    accepted_date = fields.Date('Accepted Date',
                                readonly=True)
    accepted_by = fields.Many2one('res.users',
                                  string='Accepted By',
                                  readonly=True)
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
    notification_ids = fields.One2many('mail.message', 'res_id',
                                       string='Notifications',
                                       domain=[('model', '=', 'reception')])
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
        Reduce the size of the images.
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
        Generate the code.
        User is saved and date received.
        Set to state received.
        :return:
        """
        self.received_by = self.env.user
        self.received_date = datetime.today().strftime(
            DEFAULT_SERVER_DATETIME_FORMAT)
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
        User is saved and date accepted.
        Set to state accepted.
        :return:
        """
        self.accepted_by = self.env.user
        self.accepted_date = datetime.today().strftime(
            DEFAULT_SERVER_DATETIME_FORMAT)
        self._send_first_notification()
        self.state = 'accepted'

    def print_reception_label(self):
        """
        Print the labels.
        :return:
        """
        self.ensure_one()
        return self.env.ref('aut_process.report_reception_label_id'). \
            report_action(None, data={})

    @api.multi
    def action_send_ddt_error_notification(self):
        """
        Notifica al cliente
        :return:
        """
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('aut_process','email_template_reception_ddt_error')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'reception',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }


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
