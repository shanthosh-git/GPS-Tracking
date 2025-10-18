/** @odoo-module **/

import { Component, onMounted, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";

export class MapView extends Component {
    static template = "employee_gps_tracking.MapView";
    static props = {};

    setup() {
        this.mapRef = useRef("mapCanvas");

        onMounted(async () => {
            // Wait until DOM is truly ready
            await this._waitForElement(this.mapRef);
            await this._loadGoogleMaps();
            this._renderMap();
        });
    }

    async _waitForElement(ref) {
        // retry until element exists (helps when Odoo mounts slowly)
        let retries = 0;
        while ((!ref.el || !document.body.contains(ref.el)) && retries < 20) {
            await new Promise((r) => setTimeout(r, 100));
            retries++;
        }
    }

    async _loadGoogleMaps() {
        if (typeof google !== "undefined" && google.maps) {
            return Promise.resolve();
        }
        return new Promise((resolve, reject) => {
            const existing = document.querySelector("script[src*='maps.googleapis.com']");
            if (existing) {
                existing.onload = () => resolve();
                return;
            }

            const script = document.createElement("script");
            script.src = "https://maps.googleapis.com/maps/api/js?key=AIzaSyAOBCkcBNfaHnfEqt1wm26MQeeVqhejN7E";
            script.async = true;
            script.defer = true;
            script.onload = () => resolve();
            script.onerror = (err) => reject(err);
            document.head.appendChild(script);
        });
    }

    _renderMap() {
        const container = this.mapRef.el;
        if (!container) {
            console.error("❌ Map container still not found.");
            return;
        }

        const mapOptions = {
            center: { lat: 21.7679, lng: 72.1522 },
            zoom: 8,
            mapTypeId: google.maps.MapTypeId.ROADMAP,
        };

        new google.maps.Map(container, mapOptions);
    }
}

registry.category("actions").add("employee_gps_tracking.map", MapView);
