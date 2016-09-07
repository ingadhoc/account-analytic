# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, fields


class AccountAnalyticInvoiceLine(models.Model):
    _inherit = 'account.analytic.invoice.line'
    _order = 'sequence'

    sequence = fields.Integer(
        'Sequence',
        required=True,
        default=10,
        help="The sequence field is used to order lines"
    )
