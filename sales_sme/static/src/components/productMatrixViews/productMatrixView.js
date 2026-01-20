/* @odoo-module */
import { Component, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class ProductMatrix extends Component {
    static template = "sales_sme.ProductMatrixView";

    setup() {
        this.products = [];

        onWillStart(async () => {
            const productsFromServer = await this.env.rpc({
                model: "product.template",
                method: "search_read",
                args: [[], ["name", "list_price"]],
            });

            this.products = productsFromServer;
        });
    }
}

registry.category("actions").add(
    "sales_sme.action_product_matrix_view",
    ProductMatrix
);
