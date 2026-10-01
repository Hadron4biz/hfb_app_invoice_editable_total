# -*- coding: utf-8 -*-
# vim: tabstop=4 softtabstop=0 shiftwidth=4 smarttab expandtab fileformat=unix
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
{
    'name': "Editable Invoice Total",
    'summary': "Manually override the total on draft vendor bills",
    'description': """
Editable Invoice Total
=======================

Lets you manually set the Total amount on a draft vendor bill / refund /
receipt, e.g. when the amount on the supplier's paper invoice does not match
the sum of the entered lines.

The difference is booked as a single, untaxed correction line - your real
invoice lines and their VAT amounts are never touched, and the invoice stays
balanced (Total = sum of lines) so it survives Confirm.
""",
    'version': "20.0.1.0.0",
    'author': "Hadron for Business sp. z o.o.",
    'website': "http://hadronforbusiness.com",
    'license': "OPL-1",
    'category': "Accounting/Accounting",
    'depends': [
        'account',
    ],
    'data': [],
    'images': [
        'static/description/banner_screenshot.png',
    ],
    'assets': {
        'web.assets_backend': [
            'hfb_app_invoice_editable_total/static/src/components/tax_totals_editable/tax_totals_editable.js',
            'hfb_app_invoice_editable_total/static/src/components/tax_totals_editable/tax_totals_editable.xml',
        ],
    },
    'installable': True,
    'application': False,
}
