# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api


class account_analytic_invoice_line(models.Model):
    _inherit = "account.analytic.invoice.line"

    discount = fields.Float('Discount')
    price_subtotal = fields.Float(compute='_amount_line')

    # replaced the original function to add the calculation of subtotal
    # discount
    @api.one
    def _amount_line(self):
        price_unit = self.price_unit
        if self.discount:
            price_unit = self.price_unit - \
                (self.price_unit * self.discount) / 100
        self.price_subtotal = self.quantity * price_unit
        if self.analytic_account_id.pricelist_id:
            cur = self.analytic_account_id.pricelist_id.currency_id
            self.price_subtotal = cur.round(self.price_subtotal)


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    @api.model
    def _prepare_invoice_line(self, line, fiscal_position):
        values = super(account_analytic_account, self)._prepare_invoice_line(
            line, fiscal_position)
        values['discount'] = line.discount
        return values
