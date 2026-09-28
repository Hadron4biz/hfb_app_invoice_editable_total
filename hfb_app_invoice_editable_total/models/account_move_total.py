# -*- coding: utf-8 -*-
#################################################################################
#
# Odoo, Open Source Management Solution
# Copyright (C) 2017-2026 Hadron for Business sp. z o.o. (http://hadronforbusiness.com)
#
# This program is proprietary software, licensed under the Odoo Proprietary
# License v1.0 (OPL-1). Its use is governed by the Odoo Apps terms available
# at https://www.odoo.com/documentation/user/legal/licenses.html and the
# license agreement accepted at purchase / installation.
#
# It is forbidden to publish, distribute, sublicense, or sell copies of the
# Software or modified copies of the Software.
#
# The above copyright notice and this permission notice must be included in
# all copies or substantial portions of the Software.
#
#################################################################################
""" @version	17.0.1.0.0
	@owner  Hadron for Business
	@author Hadron for Business sp. z o.o.
	@date   2026.09.14

	Editable Invoice Total
	Lets the user manually override the Total on a draft vendor bill /
	refund / receipt. The difference between the entered lines and the
	requested total is booked onto a single, untaxed correction line, so
	VAT on the real lines is never touched and the invoice stays balanced
	(Total = sum of lines) through Confirm.
"""
from odoo import _, models

PURCHASE_MOVE_TYPES = ('in_invoice', 'in_refund', 'in_receipt')


class AccountMove(models.Model):
    _inherit = 'account.move'

    def action_set_manual_total(self, new_total):
        """Matches the invoice Total to a value entered manually by the user
        on a draft vendor bill (e.g. the supplier's invoice shows a
        different total than what the entered lines add up to).

        The difference is booked onto a single, untaxed correction line
        (not spread over the existing tax rates), so that:
          - the VAT amounts on the real lines stay untouched,
          - Total still equals the sum of lines, so the record stays
            balanced and survives Confirm.

        Note: the correction line is found again on a later call by
        matching its translated name - if this method is ever called for
        the same invoice under different user languages, it will create a
        second correction line instead of updating the first one. Fine for
        a single-language deployment; a stable technical marker (e.g. a
        boolean field on the line) would be needed to support mixed
        languages on the same invoice.
        """
        self.ensure_one()
        if self.move_type not in PURCHASE_MOVE_TYPES or self.state != 'draft':
            return False

        correction_name = _('Manual correction (matched to vendor invoice total)')
        correction_line = self.invoice_line_ids.filtered(
            lambda l: l.name == correction_name)
        other_lines = self.invoice_line_ids - correction_line
        current_correction_amount = sum(correction_line.mapped('price_subtotal'))
        total_without_correction = self.amount_total - current_correction_amount
        delta = new_total - total_without_correction

        if correction_line:
            if delta:
                correction_line.price_unit = delta
            else:
                correction_line.unlink()
        elif delta:
            fallback_account = other_lines[-1:].account_id or self.journal_id.default_account_id
            self.invoice_line_ids = [(0, 0, {
                'name': correction_name,
                'quantity': 1,
                'price_unit': delta,
                'tax_ids': [(5, 0, 0)],
                'account_id': fallback_account.id if fallback_account else False,
            })]
        return True

#EoF
