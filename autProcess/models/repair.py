# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, tools, _
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