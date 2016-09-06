# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api


class account_analytic_account(models.Model):
    _inherit = "account.analytic.account"

    @api.multi
    def update_lines_prices_from_products(self):
        for contract in self:
            for line in contract.recurring_invoice_line_ids:
                partner = line.analytic_account_id.partner_id
                pricelist = line.analytic_account_id.pricelist_id
                vals = line.product_id_change(
                    line.product_id.id, line.uom_id.id, qty=line.quantity,
                    name=line.name, partner_id=partner.id, price_unit=False,
                    pricelist_id=pricelist.id, company_id=None).get(
                    'value', {})
                price_unit = vals.get('price_unit')
                line.price_unit = price_unit
