##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import fields, models


class AccountAnalyticAccountDistribution(models.Model):
    _name = "account.analytic.account.distribution_line"

    distribution_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Distribution Account',
        index=True,
        required=True,
        ondelete='cascade',
    )
    account_analytic_id = fields.Many2one(
        'account.analytic.account',
        'Analytic Account',
        required=True,
    )
    percentage = fields.Float(
        required=True,
    )
