# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in module root
# directory
##############################################################################
from openerp import models, api
# from openerp.exceptions import Warning
import logging
_logger = logging.getLogger(__name__)


class AccountInvoice(models.Model):
    _inherit = "account.invoice"

    @api.multi
    def finalize_invoice_move_lines(self, move_lines):
        """ finalize_invoice_move_lines(move_lines) -> move_lines

            Odoo Hook method to be overridden in additional modules to verify
            and possibly alter the move lines to be created by an invoice, for
            special cases.
            :param move_lines: list of dictionaries with the account.move.lines
                (as for create())
            :return: the (possibly updated) final move_lines to create for this
                invoice
        """
        move_lines = super(
            AccountInvoice, self).finalize_invoice_move_lines(move_lines)
        new_move_lines = []
        for a, b, move_line in move_lines:
            analytic = self.env['account.analytic.account'].browse(
                move_line['analytic_account_id'])
            if analytic.is_distribution:
                analytic.check_distribution_lines()
                remaining_lines = len(analytic.distribution_line_ids)
                # we do this way because of rounding erros, we use residual
                # on last line
                amount_currency = amount_currency_residual = move_line[
                    'amount_currency']
                debit = debit_residual = move_line['debit']
                credit = credit_residual = move_line['credit']
                for dist_line in analytic.distribution_line_ids:
                    inv_round = self.company_id.currency_id.round
                    percentage = dist_line.percentage / 100.0
                    new_account_id = dist_line.account_analytic_id.id
                    if remaining_lines == 1:
                        new_line_amount_currency = amount_currency_residual
                        new_line_debit = inv_round(debit_residual)
                        new_line_credit = inv_round(credit_residual)
                    else:
                        new_line_debit = debit and inv_round(
                            debit * percentage)
                        new_line_credit = credit and inv_round(
                            credit * percentage)
                        new_line_amount_currency = (
                            amount_currency and inv_round(
                                amount_currency * percentage))
                        amount_currency_residual -= new_line_amount_currency
                        debit_residual -= new_line_debit
                        credit_residual -= new_line_credit
                        # esto es para cuando son importes chicos y porcentajes
                        # chicos y como el redondeo es para arriba, llega un
                        # momento donde puede no haber mas saldo entonces
                        # forzamos el cierre del balance aca y luego la linea
                        # de cierre se hace en cero
                        if credit_residual < 0.0:
                            new_line_credit += credit_residual
                            credit_residual = 0.0
                        if debit_residual < 0.0:
                            new_line_debit += debit_residual
                            debit_residual = 0.0
                    remaining_lines -= 1
                    new_line = move_line.copy()
                    new_line['analytic_account_id'] = new_account_id
                    new_line['amount_currency'] = new_line_amount_currency
                    new_line['credit'] = new_line_credit
                    new_line['debit'] = new_line_debit

                    for c, d, analytic_line in new_line['analytic_line_ids']:
                        analytic_line['amount'] = (
                            analytic_line['amount'] * percentage)
                        analytic_line['account_id'] = new_account_id
                    new_move_lines.append((0, 0, new_line))
            else:
                new_move_lines.append((0, 0, move_line))

        return new_move_lines
