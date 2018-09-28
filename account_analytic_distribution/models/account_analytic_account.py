##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import  api, fields, models, _
from odoo.exceptions import ValidationError


class AccountAnalyticAccount(models.Model):
    _inherit = "account.analytic.account"

    is_distribution = fields.Boolean(
    )
    distribution_line_ids = fields.One2many(
        'account.analytic.account.distribution_line',
        'distribution_analytic_id',
        'Distribution Line',
    )

    @api.constrains('distribution_line_ids', 'is_distribution')
    def check_distribution_lines(self):
        for rec in self:
            difference = rec.company_id.currency_id.round(sum(
                rec.distribution_line_ids.mapped('percentage')) - 100.0)
            if rec.is_distribution and difference:
                raise ValidationError(_(
                    'Lines of the analytic distribuion account "%s" must '
                    'sum 100') % rec.name)
