/** @odoo-module **/

// 20.0 note: Odoo 20 moved to Owl 3 - TaxTotalsComponent.totals is now a
// computed signal read as this.totals(), DOM refs are signal.ref() objects
// read by calling them, and reactive state is created with proxy() instead of
// useState(). The patch below follows the same patterns the native
// TaxGroupComponent uses.

import { patch } from "@web/core/utils/patch";
import { parseFloat } from "@web/views/fields/parsers";
import { formatFloat } from "@web/core/utils/numbers";
import { useService } from "@web/core/utils/hooks";
import { onPatched, proxy, signal } from "@odoo/owl";
import { TaxTotalsComponent } from "@account/components/tax_totals/tax_totals";

// Vendor bills / refunds / receipts only - same restriction the native
// read-only totals widget applies on account.view_move_form.
const PURCHASE_MOVE_TYPES = ["in_invoice", "in_refund", "in_receipt"];

patch(TaxTotalsComponent.prototype, {
    setup() {
        super.setup();
        this.notification = useService("notification");
        this.totalValueInput = signal.ref();
        this.totalState = proxy({ value: "readonly" });
        onPatched(() => {
            const el = this.totalValueInput();
            if (this.totalState.value === "edit" && el) {
                el.value = formatFloat(this.totals().total_amount_currency);
                el.focus();
            }
        });
    },

    get totalEditable() {
        return (
            !this.readonly &&
            PURCHASE_MOVE_TYPES.includes(this.props.record.data.move_type) &&
            !!this.props.record.resId
        );
    },

    setTotalState(value) {
        this.totalState.value = ["readonly", "edit", "disable"].includes(value) ? value : "readonly";
    },

    /**
     * The user typed a new value for the Total. Total isn't a plain field
     * but a value computed from the invoice lines, so to make the change
     * actually stick (and survive Confirm), we call the backend method
     * account.move.action_set_manual_total, which books the difference as
     * a dedicated, untaxed correction line (the VAT amounts on the real
     * lines are left untouched). The current form is saved first, so we
     * don't lose any other unsaved changes the user made.
     */
    async _onChangeTotalValue() {
        const el = this.totalValueInput();
        if (!el || this.totalState.value !== "edit") {
            return;
        }
        this.setTotalState("disable");
        const oldValue = this.totals().total_amount_currency;
        let newValue;
        try {
            newValue = parseFloat(el.value);
        } catch {
            this.setTotalState("edit");
            return;
        }
        if (newValue === oldValue) {
            this.setTotalState("readonly");
            return;
        }

        try {
            await this.props.record.save();
            await this.orm.call("account.move", "action_set_manual_total", [
                [this.props.record.resId],
                newValue,
            ]);
            await this.props.record.model.load();
        } catch (error) {
            this.notification.add(error.message || String(error), { type: "danger" });
        }
        this.setTotalState("readonly");
    },
});
