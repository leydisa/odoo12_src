# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class Notification(models.Model):
    """
    Class Notification.
    """
    _name = "notification"

    def _send_notification(self, template):
        """
        Send notification.
        :return:
        """
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('aut_process',
                                                             template)[1]
        except ValueError:
            template_id = False
        self.env['mail.template'].browse(template_id).send_mail(self.id,
                                                                force_send=True)
        return True
