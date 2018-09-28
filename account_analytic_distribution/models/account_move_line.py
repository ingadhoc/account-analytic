##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import api, models, _
from odoo.exceptions import ValidationError


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.constrains('analytic_account_id')
    def check_is_distribution(self):
        for rec in self.filtered(
                lambda x: x.analytic_account_id.is_distribution):
            raise ValidationError(_(
                'You can not choose an analytic account of type "Distribution"'
                ' on a journal entry, you need to split lines manually'))
