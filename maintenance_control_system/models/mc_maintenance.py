# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.


from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class McMaintenance(models.Model):
    """
    Maintenance.
    """
    _description = 'Maintenance'
    _inherit = ['doc.state']
    _name = 'mc.maintenance'
    _rec_name = 'code'

    def _get_default_date(self):
        """
        :return: to the date of the day
        """
        date = fields.Date.from_string(fields.Date.today())
        return '{}-01-01'.format(date)

    def _get_default_partner1(self):
        """
        :return: to the date of the day
        """
        if self.env.context.get('type') in ('imp', 'emp'):
            year = fields.Date.from_string(fields.Date.today()).year
            ids = self.env['mc.budget.to.provided'].search([('year', '=', year)]).mapped('entity_id').ids
            dom = [('supplier', '=', False)]
            dom += [('type', '=', 'internal')]
            dom += [('id', 'in', ids)]
            partner_ids = self.env['mc.partner'].search(dom)
            if len(partner_ids) == 1:
                return partner_ids[0]

    def _default_current_labor_coste(self):
        """
        Calculate the current cost of labor for maintenance provided.
        :return:
        """
        if self.env.context.get('type') == 'mr':
            return False
        labor = self.env['mc.labor'].search([], limit=1, order='date desc')
        if len(labor) == 0:
            raise ValidationError(_('Define the cost of labor.'))
        else:
            return labor

    @api.one
    @api.depends('line_ids', 'labor_hours', 'labor_days', 'labor_technicians')
    def _compute_coste(self):
        """
        Calculate the current price of the material.
        :return:
        """
        self.coste_cuc = sum([x.qty * x.equipment_id.coste_cuc for x in self.line_ids]) + \
            (self.labor_days * self.labor_hours * self.labor_technicians * self.labor_id.coste_cuc
             if self.labor_id else 0)
        self.coste_cup = sum([x.qty * x.equipment_id.coste_cup for x in self.line_ids]) + \
            (self.labor_days * self.labor_hours * self.labor_technicians * self.labor_id.coste_cup
            if self.labor_id else 0)
        self.mt = self.coste_cuc + self.coste_cup

    @api.constrains('datetime_start', 'datetime_stop', 'mt')
    def _check_data(self):
        """
        It is checked that the start date / time is less than the final date.
        :return:
        """
        if fields.Datetime.from_string(self.datetime_start) >= fields.Datetime.from_string(self.datetime_stop):
            raise ValidationError(_('The start date / time must be less than the final date.'))

    code = fields.Char(string='Code',
                       readonly=True,
                       default=_('New'))
    date = fields.Date(string='Creation Date',
                       required=True,
                       index=True,
                       default=_get_default_date)
    datetime_start = fields.Datetime(string="",
                                     required=True)
    datetime_stop = fields.Datetime(string="",
                                    required=True)
    user_id = fields.Many2one('res.users',
                              string='Created by',
                              readonly=True,
                              default=lambda self: self.env.user.id)
    partner_id = fields.Many2one('mc.partner',
                                 ondelete='restrict')
    contract_id = fields.Many2one('mc.contract',
                                  string='Contract',
                                  ondelete='restrict',
                                  domain="[('partner_id', '=', partner_id), "
                                         "('state', '=', 'finalized'),"
                                         "('date', '<=', date),"
                                         "'|', ('expiration_date', '>=', date),"
                                         "('expiration_date', '=', False)]")
    province_id = fields.Many2one(string='Province',
                                  related='partner_id.province_id',
                                  readonly=True)
    partner1_id = fields.Many2one('mc.partner',
                                  ondelete='restrict',
                                  default=_get_default_partner1)
    contract1_id = fields.Many2one('mc.contract',
                                   string='Contract',
                                   ondelete='restrict',
                                   domain="[('partner_id', '=', partner1_id), "
                                          "('state', '=', 'finalized'),"
                                          "('date', '<=', date),"
                                          "'|', ('expiration_date', '>=', date),"
                                          "('expiration_date', '=', False)]")
    province1_id = fields.Many2one(string='Province',
                                   related='partner1_id.province_id',
                                   readonly=True)
    type = fields.Selection([('imp', 'Internal Maintenance Provided'),
                             ('emp', 'External Maintenance Provided'),
                             ('mr', 'External Maintenance Received')],
                            string='Type',
                            default=lambda self: self.env.context.get('type') or False)
    observation = fields.Text('Observation',
                              required=True)
    invoice = fields.Binary(string='Invoice')
    invoice_filename = fields.Char('Invoice')
    work_order_id = fields.Many2one('mc.work.order',
                                    'Work Order',
                                    readonly=True,
                                    ondelete='restrict')
    labor_id = fields.Many2one('mc.labor',
                               string="Labor",
                               default=_default_current_labor_coste,
                               ondelete='restrict')
    labor_days = fields.Integer('Worked Days')
    labor_hours = fields.Float('Hours Worked/Day')
    labor_technicians = fields.Integer('Technicians')
    line_ids = fields.One2many('mc.maintenance.line', 'maintenance_id',
                               string='Lines')
    coste_cuc = fields.Float(string='CUC',
                             compute=_compute_coste,
                             store=True)
    coste_cup = fields.Float(string='CUP',
                             compute=_compute_coste,
                             store=True)
    mt = fields.Float(string='MT',
                      compute=_compute_coste,
                      store=True)

    @api.multi
    def unlink(self):
        """
        It is not possible to delete in the finalized state.
        :return:
        """
        if self.state == 'finalized':
            raise ValidationError('It is not possible to delete in the finalized state.')
        return super(McMaintenance, self).unlink()

    @api.onchange('date')
    def _onchange_date(self):
        if not self.date:
            self.partner_id = False
            self.partner1_id = False

    @api.onchange('partner_id', 'date')
    def _onchange_partner_id(self):
        """
        If the customer or supplier has only one contract, it is shown by default.
        :return:
        """
        self.contract_id = False
        if self.partner_id and self.env.context.get('type') == 'emp':
            dom = [('partner_id', '=', self.partner_id.id), ('date', '<=', self.date),
                   '|', ('expiration_date', '>=', self.date), ('expiration_date', '=', False)]
            contract_ids = self.env['mc.contract'].search(dom)
            if len(contract_ids) == 1:
                self.contract_id = contract_ids[0]

    @api.onchange('partner1_id', 'date')
    def _onchange_partner1_id(self):
        """
        If the customer or supplier has only one contract, it is shown by default.
        :return:
        """
        self.contract1_id = False
        if self.partner1_id and self.env.context.get('type') == 'mr':
            dom = [('partner_id', '=', self.partner1_id.id), ('date', '<=', self.date),
                   '|', ('expiration_date', '>=', self.date), ('expiration_date', '=', False)]
            contract_ids = self.env['mc.contract'].search(dom)
            if len(contract_ids) == 1:
                self.contract1_id = contract_ids[0]

    @api.one
    def action_finalized(self):
        """
        Check data.
        Generate the code.
        Update the budget used.
        :return:
        """
        # Check data
        if len(self.line_ids) == 0:
            raise ValidationError(_('Missing maintenance detail.'))
        if self.mt == 0:
            raise ValidationError(_('You cannot finalized maintenance with cost 0.'))
        # Generate the code
        if self.type == 'mr':
            self.code = self.env['ir.sequence'].next_by_code('mc.maintenance.received.sequence')
        elif self.type == 'imp':
            self.code = self.env['ir.sequence'].next_by_code('mc.internal.maintenance.provided.sequence')
        else:
            self.code = self.env['ir.sequence'].next_by_code('mc.external.maintenance.provided.sequence')
        # Update the budget used
        year = fields.Datetime.from_string(self.date).year
        if self.type == 'mr':
            model = 'mc.budget.to.received'
            entity_id = self.partner_id.id
        else:
            model = 'mc.budget.to.provided'
            entity_id = self.partner1_id.id
        budget = self.env[model].search([('year', '=', year), ('entity_id', '=', entity_id)], limit=1)
        budget.used_cuc = self.coste_cuc
        budget.used_cup = self.coste_cup
        return super(McMaintenance, self).action_finalized()


class McMaintenanceLine(models.Model):
    """
    Class Maintenance Line.
    """
    _description = 'Maintenance Line'
    _name = "mc.maintenance.line"

    maintenance_id = fields.Many2one('mc.maintenance',
                                     ondelete='cascade')
    equipment_id = fields.Many2one('mc.equipment',
                                   required=True,
                                   ondelete='restrict')
    qty = fields.Integer(string='Quantity',
                         required=True)
    coste_cuc = fields.Float(string='CUC)',
                             related='equipment_id.coste_cuc',
                             readonly=True)
    coste_cup = fields.Float(string='CUP',
                             related='equipment_id.coste_cup',
                             readonly=True)

    _sql_constraints = [
        ('equipment_uniq', 'unique (maintenance_id, equipment_id)', 'Repeated equipment!'),
        ('qty_zero', 'CHECK (qty > 0)', 'Number of equipment greater than 0!'),
    ]