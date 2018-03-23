##############################################################################
# For copyright and license notices, see __manifest__.py file in module root
# directory
##############################################################################
from odoo import models, api, _
from odoo.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.one
    @api.constrains('analytic_account_id')
    def check_is_distribution(self):
        if self.analytic_account_id.is_distribution:
            raise Warning(_(
                'You can not choose an analytic account of type "Distribution"'
                ' on a journal entry, you need to split lines manually'))
