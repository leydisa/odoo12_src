# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import datetime
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


def _get_years():
    year_list = []
    for i in range(2018, datetime.datetime.now().year + 1):
        year_list.append((str(i), str(i)))
    return year_list


class McPartner(models.Model):
    """
    Class that represent customer and supplier.
    """
    _description = 'Partner'
    _name = "mc.partner"

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    code = fields.Char(string='Code',
                       readonly=True,
                       default=_('New'))
    name = fields.Char(index=True,
                       required=True)
    image = fields.Binary("Image",
                          attachment=True,
                          help="This field holds the image used as avatar for this contact, limited to 1024x1024px")
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    province_id = fields.Many2one('mc.province',
                                  required=True,
                                  ondelete='restrict')
    email = fields.Char(string='Email',
                        required=True)
    phone = fields.Char(string='Phone',
                        required=True)
    supplier = fields.Boolean(string='Is a Vendor',
                              default=lambda self: self.env.context.get('supplier') or False)
    type = fields.Selection([('internal', 'Internal'),
                             ('external', 'External')],
                            string='Type',
                            default=lambda self: self.env.context.get('type') or False)
    active = fields.Boolean(default=True)
    budget_to_received_ids = fields.One2many('mc.budget',
                                             ondelete='cascade')
    budget_to_received_ids = fields.One2many('mc.budget.to.received', 'entity_id',
                                             string='To Received')
    budget_to_provided_ids = fields.One2many('mc.budget.to.provided', 'entity_id',
                                             string='To Provided')

    _sql_constraints = [
        ('name_uniq', 'unique(name)', 'Name must be unique!'),
    ]

    @api.model
    def create(self, vals):
        """
        Generate the code.
        :param vals:
        :return:
        """
        if vals['supplier']:
            vals['code'] = self.env['ir.sequence'].next_by_code('mc.supplier.sequence')
        else:
            sequence = 'mc.%s.customer.sequence' % vals['type']
            vals['code'] = self.env['ir.sequence'].next_by_code(sequence)
        return super(McPartner, self).create(vals)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        date = self._context.get('date', False)
        if 'type' in self._context and not date:
            args = [('id', '=', 0)]
        type = self._context.get('type', False)
        year = fields.Datetime.from_string(date).year
        if type == 'mr' and date:
            ids = self.env['mc.budget.to.received'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        elif type == 'mr1':
            args += [('supplier', '=', True)]
        elif type == 'imp':
            ids = self.env['mc.budget.to.received'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        elif type == 'imp1':
            ids = self.env['mc.budget.to.provided'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        elif type == 'emp':
            args += [('supplier', '=', False)]
            args += [('type', '=', 'external')]
        elif type == 'emp1':
            ids = self.env['mc.budget.to.provided'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        return super(McPartner, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class McBudgetToReceived(models.Model):
    """
    Class that represent Annual Budget.
    """
    _description = 'Annual Budget'
    _name = "mc.budget.to.received"

    # def add_maintenance_provided(self, date, cuc, cup):
    #     """
    #
    #     :param cuc:
    #     :param cup:
    #     :return:
    #     """
    #     year = fields.Datetime.from_string(date).year
    #     budget = self.search([('year', '=', year)], limit=1)
    #     if len(budget) == 0:
    #         raise ValidationError(_('Define the budget for the current year.'))
    #     else:
    #         budget.write({'used_provided_cuc': budget.used_provided_cuc + cuc,
    #                       'percent_provided_cuc': ((budget.used_provided_cuc + cuc) * 100)
    #                                               / budget.budget_provided_cuc,
    #                       'used_provided_cup': budget.used_provided_cup + cup,
    #                       'percent_provided_cup': ((budget.used_provided_cup + cup) * 100)
    #                                               / budget.budget_provided_cup})

    # def add_maintenance_received(self, date, cuc, cup):
    #     """
    #
    #     :param cuc:
    #     :param cup:
    #     :return:
    #     """
    #     year = fields.Datetime.from_string(date).year
    #     budget = self.search([('year', '=', year)], limit=1)
    #     if len(budget) == 0:
    #         raise ValidationError(_('Define the budget for the current year.'))
    #     else:
    #         budget.write({'used_received_cuc': budget.used_received_cuc + cuc,
    #                       'percent_received_cuc': ((budget.used_received_cuc + cuc) * 100)
    #                                               / budget.budget_received_cuc,
    #                       'used_received_cup': budget.used_received_cup + cup,
    #                       'percent_received_cup': ((budget.used_received_cup + cup) * 100)
    #                                               / budget.budget_received_cup})

    def _get_default_year(self):
        """
        :return: to the current year
        """
        return str(datetime.datetime.now().year)

    year = fields.Selection(_get_years(),
                            string='Year',
                            required=True,
                            default=_get_default_year)
    entity_id = fields.Many2one('mc.partner',
                                required=True,
                                ondelete='cascade')
    budget_cuc = fields.Float("CUC",
                              required=True)
    budget_cup = fields.Float("CUP",
                              required=True)
    used_cuc = fields.Float("CUC",
                            readonly=True)
    used_cup = fields.Float("CUP",
                            readonly=True)
    percent_cuc = fields.Float("CUC",
                               readonly=True)
    percent_cup = fields.Float("CUP",
                               readonly=True)

    _sql_constraints = [
        ('budget_zero', 'CHECK (budget_cuc > 0 and budget_cup > 0)', 'The budget must be greater than 0.'),
        ('year_unique', 'unique(entity_id, year)', 'Repeated year!'),
    ]


class McBudgetToProvided(models.Model):
    """
    Class that represent Annual Budget.
    """
    _description = 'Annual Budget'
    _name = "mc.budget.to.provided"
    _inherit = "mc.budget.to.received"
