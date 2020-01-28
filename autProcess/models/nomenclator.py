# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _


class NomenclatorType(models.Model):
    """
    Class that represent Nomenclator Type.
    """
    _name = 'nomenclator.type'
    _rec_name = 'name'
    _description = 'Nomenclator Type'

    code = fields.Char(string='Code',
                       required=True)
    name = fields.Char(string='Name',
                       required=True)


class Nomenclator(models.Model):
    """
    Class that represent Nomenclator.
    """
    _name = 'nomenclator'
    _rec_name = 'name'
    _description = 'Nomenclator'

    def _default_type_id(self):
        """

        :return:
        """
        if 'type' in self._context:
            return self.env['nomenclator.type'].\
                search([('code', '=', self._context['type'])], limit=1).id
        else:
            return False

    type_id = fields.Many2one('nomenclator.type',
                              required=True,
                              ondelete='cascade',
                              default=_default_type_id)
    code = fields.Char(string='Code')
    name = fields.Char(string='Name',
                       required=True)

