# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from . import common
from .common import FIRST_CUSTOMER_NOTIFICATION


class Repair(models.Model):
    """
    Class representing a repair.
    """
    _name = 'repair'
    _rec_name = 'code'
    _description = 'Repair'

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    @api.multi
    @api.constrains('attachment_ids')
    def _check_data(self):
        """
        La cantidad de fotos del paquete abierto debe ser como minimo 3.
        :return:
        """
        if len(self.attachment_ids) < 3:
            raise ValidationError(_('Al menos debe registrar 3 fotos del paquete abierto'))

    code = fields.Char(string='RMA',
                       required=True,
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       readonly=True,
                       index=True,
                       default=_get_default_date)
    date_accept = fields.Date('Acceptance Date')
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)
    photo1 = fields.Binary("Photo 1")
    photo2 = fields.Binary("Photo 2")
    photo3 = fields.Binary("Photo 3")
    photo4 = fields.Binary("Photo 4")
    photo5 = fields.Binary("Photo 5")
    ddt = fields.Binary("DDT")
    attachment_ids = \
        fields.Many2many('ir.attachment',
                         'repair_attachments_rel',
                         'repair_id', 'attachment_id',
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
    equipment_ids = fields.One2many('repair.equipment', 'repair_id',
                                    string='Equipos')
    type_id = fields.Many2one('nomenclator',
                              string='Type',
                              required=True,
                              domain=[('type_id.code', '=', 'equipment_type')])
    symptom_id = fields.Many2one('nomenclator',
                                 string='Symptom',
                                 required=True,
                                 domain=[('type_id.code', '=', 'symptom_type')])
    diagnosis_id = fields.Many2one('nomenclator',
                                   string='Diagnosis',
                                   required=True,
                                   domain=[('type_id.code', '=', 'diagnosis_type')])
    observation = fields.Text('Observation')
    state = fields.Selection([('draft', 'Draft'),
                              ('received', 'Received'),
                              ('closed', 'Closed'),
                              ('cancel', 'Cancel')],
                             string='State',
                             default='draft')
    cancel_reason = fields.Text('Reason for Cancellation')

    _sql_constraints = [
        ('code_uniq', 'unique(code)',
         'The RMA must be unique!')
    ]

    @api.multi
    def write(self, vals):
        """

        :param vals:
        :return:
        """
        tools.image_resize_images(vals)
        return super(Repair, self).write(vals)

    @api.one
    def action_received(self):
        """
        Generate the RMA code.
        Set to state received.
        :return:
        """
        self.code = self.env['ir.sequence'].next_by_code('repair.sequence')
        self.state = 'received'

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


class RepairEquipment(models.Model):
    """
    Class representing the equipment of a repair.
    """
    _name = 'repair.equipment'
    _rec_name = 'equipment_id'
    _description = 'Equipment of a repair'

    repair_id = fields.Many2one('repair',
                                ondelete='cascade')
    equipment_id = fields.Many2one('equipment',
                                   string='Serial',
                                   required=True)
    type_id = fields.Many2one(related='equipment_id.type_id')
    description = fields.Char(related='equipment_id.description')