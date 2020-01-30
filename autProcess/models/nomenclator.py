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

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False,
                        submenu=False):
        """
        If it comes in readonly context it is not allowed to create or delete.
        :param view_id:
        :param view_type:
        :param toolbar:
        :param submenu:
        :return:
        """
        res = super(Nomenclator, self).fields_view_get(view_id, view_type,
                                                       toolbar=toolbar,
                                                       submenu=False)
        if view_type == 'tree' and self._context.get('readonly', False):
            res['arch'] = res['arch'].\
                replace('<tree string="Nomenclator">',
                        '<tree delete="false" create="false">')
        return res