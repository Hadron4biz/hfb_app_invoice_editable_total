# Editable Invoice Total

Lets you manually set the **Total** amount on a draft vendor bill / refund /
receipt - e.g. when the amount on the supplier's paper invoice doesn't match
the sum of the lines you entered.

## How it works

Click the pencil next to the Total on a draft vendor bill, type the correct
amount. The difference is booked as a single, untaxed correction line:

- your real invoice lines and their VAT amounts are never touched,
- Total still equals the sum of lines, so the invoice stays balanced and the
  change survives Confirm.

Only available on draft vendor bills / vendor credit notes / vendor receipts
(`in_invoice`, `in_refund`, `in_receipt`) - the same scope as the native
read-only totals widget.

## Technical

- `models/account_move_total.py` - `account.move.action_set_manual_total()`
- `static/src/components/tax_totals_editable/` - OWL patch of the native
  `TaxTotalsComponent` (`account.TaxTotalsField`), adds the inline edit
  affordance on the Total line.
- No new models, no data, no security rules (extends `account.move` only).
- Depends on: `account`.

## Status

Extracted from a client-specific module (`hfb_bannerstop_invoice_total`) as
a pilot run of the "generic app extraction" workflow. Not yet submitted to
Odoo Apps - missing `static/description/icon.png` and
`static/description/index.html` (Store listing page).
