# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api, _
from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class AccountAnalyticLine(models.Model):
    _inherit = "account.analytic.line"

    @api.one
    @api.constrains('account_id')
    def check_is_distribution(self):
        if self.account_id.is_distribution:
            raise Warning(_(
                'You can not choose an analytic account of type "Distribution"'
                ' on an analytic line, you need to split lines manually'))
