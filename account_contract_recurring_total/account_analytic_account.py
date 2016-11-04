# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields, api
from openerp.addons.decimal_precision import decimal_precision as dp


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    recurring_total_amount = fields.Float(
        'Recurring Total',
        compute='_compute_recurring_total_amount',
        # we dont make storable so it is compatible with contract
        # discount
        # store=True,
        digits=dp.get_precision('Account'),
    )

    @api.one
    @api.depends(
        'recurring_invoice_line_ids.quantity',
        'recurring_invoice_line_ids.price_unit',
    )
    def _compute_recurring_total_amount(self):
        self.recurring_total_amount = sum(
            self.recurring_invoice_line_ids.mapped('price_subtotal'))
