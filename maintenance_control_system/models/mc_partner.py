# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


import datetime
from odoo import api, fields, models, tools,  _


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
    image_medium = fields.Binary("Image",
                          attachment=True)
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
        tools.image_resize_images(vals)
        if vals['supplier']:
            vals['code'] = self.env['ir.sequence'].next_by_code('mc.supplier.sequence')
        else:
            sequence = 'mc.%s.customer.sequence' % vals['type']
            vals['code'] = self.env['ir.sequence'].next_by_code(sequence)
        return super(McPartner, self).create(vals)

    @api.multi
    def write(self, vals):
        tools.image_resize_images(vals)
        return super(McPartner, self).write(vals)

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        m_type = self._context.get('m_type', False)
        date = self._context.get('date', False)
        year = fields.Datetime.from_string(date).year if date else False
        if m_type == 'mr':
            ids = self.env['mc.budget.to.received'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        elif m_type == 'mr1':
            dom = [('supplier', '=', True), ('date', '<=', date), '|', ('expiration_date', '>=', date),
                    ('expiration_date', '=', False)]
            ids = self.env['mc.contract'].search(dom).mapped('partner_id').ids
            args += [('id', 'in', ids)]
        elif m_type == 'imp':
            ids = self.env['mc.budget.to.received'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'not in', ids)]
        elif m_type == 'imp1':
            ids = self.env['mc.budget.to.provided'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        elif m_type == 'emp':
            dom = [('supplier', '=', False), ('date', '<=', date), '|', ('expiration_date', '>=', date),
                   ('expiration_date', '=', False)]
            ids = self.env['mc.contract'].search(dom).mapped('partner_id').ids
            args += [('id', 'in', ids)]
        elif m_type == 'emp1':
            ids = self.env['mc.budget.to.provided'].search([('year', '=', year)]).mapped('entity_id').ids
            args += [('supplier', '=', False)]
            args += [('type', '=', 'internal')]
            args += [('id', 'in', ids)]
        elif m_type == 'etr':
            ids = self.env['mc.budget.to.received'].search([]).mapped('entity_id').ids
            args += [('id', 'in', ids)]
        elif m_type == 'etp':
            ids = self.env['mc.budget.to.provided'].search([]).mapped('entity_id').ids
            args += [('id', 'in', ids)]
        return super(McPartner, self)._name_search(name, args=args, operator=operator, limit=limit, name_get_uid=name_get_uid)


class McBudgetToReceived(models.Model):
    """
    Class that represent Annual Budget.
    """
    _description = 'Annual Budget'
    _name = "mc.budget.to.received"

    @api.depends('budget_cuc', 'used_cuc')
    @api.multi
    def _compute_percent_cuc(self):
        """
        Compute percent cuc
        :return:
        """
        self.percent_cuc = self.used_cuc * 100 / self.budget_cuc

    @api.depends('budget_cup', 'used_cup')
    @api.multi
    def _compute_percent_cup(self):
        """
        Compute percent cup
        :return:
        """
        self.percent_cup = self.used_cup * 100 / self.budget_cup

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
    budget_cuc = fields.Float("Budget (CUC)",
                              required=True)
    budget_cup = fields.Float("Budget (CUP)",
                              required=True)
    used_cuc = fields.Float("Used (CUC)",
                            readonly=True)
    used_cup = fields.Float("Used (CUP)",
                            readonly=True)
    percent_cuc = fields.Float("CUC",
                               compute="_compute_percent_cuc",
                               readonly=True,
                               store=False)
    percent_cup = fields.Float("CUP",
                               compute="_compute_percent_cup",
                               readonly=True,
                               store=False)

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
