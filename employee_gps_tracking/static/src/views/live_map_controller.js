/** @odoo-module */

import { LiveMapRenderer } from "./live_map_renderer";
import { standardViewProps } from "@web/views/view";
import { useService } from "@web/core/utils/hooks";
import { Component, onWillStart, onWillUnmount, useState } from "@odoo/owl";

export class LiveMapController extends Component {
    static components = { LiveMapRenderer };
    static template = "employee_gps_tracking.LiveMapController";
    static props = { ...standardViewProps };

    setup() {
        this.orm = useService("orm");
        this.action = useService("action");
        this.state = useState({ employees: [] });
        this.interval = null;

        onWillStart(async () => {
            await this.fetchData();
            this.startPolling();
        });

        onWillUnmount(() => {
            this.stopPolling();
        });
    }

    async fetchData() {
        const employees = await this.orm.call(
            "hr.employee",
            "get_live_employee_data",
            []
        );
        this.state.employees = employees;
    }

    startPolling() {
        this.stopPolling();
        this.interval = setInterval(async () => {
            await this.fetchData();
        }, 15000); // Refresh every 15 seconds
    }

    stopPolling() {
        if (this.interval) {
            clearInterval(this.interval);
            this.interval = null;
        }
    }
}