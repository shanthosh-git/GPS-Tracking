/** @odoo-module **/

import { Component, onMounted, onWillUnmount, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class MapView extends Component {
    static template = "employee_gps_tracking.MapView";
    static props = {};

    setup() {
        this.mapRef = useRef("mapCanvas");
        this.orm = useService("orm");
        this.markers = [];
        this.interval = null;

        onMounted(async () => {
            await this._waitForElement(this.mapRef);
            await this._loadGoogleMaps();
            this._renderMap();
            this._getAndRenderEmployees();
            this.interval = setInterval(() => this._getAndRenderEmployees(), 10000); // Refresh every 10 seconds
        });

        onWillUnmount(() => {
            if (this.interval) {
                clearInterval(this.interval);
            }
        });
    }

    async _waitForElement(ref) {
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
            minZoom: 2, // Prevent zooming out too far
            mapTypeId: google.maps.MapTypeId.ROADMAP,
        };

        this.map = new google.maps.Map(container, mapOptions);
    }

    async _getAndRenderEmployees() {
        const employeeData = await this.orm.call(
            "hr.employee",
            "get_live_employee_data",
            []
        );

        console.log("Live employee location data from server:", employeeData);

        // Clear existing markers
        this.markers.forEach(marker => marker.setMap(null));
        this.markers = [];

        employeeData.forEach(employee => {
            const marker = new google.maps.Marker({
                position: { lat: employee.latest_latitude, lng: employee.latest_longitude },
                map: this.map,
                title: employee.name,
            });

            const infoWindow = new google.maps.InfoWindow({
                content: `<h5>${employee.name}</h5>`
            });

            marker.addListener('click', () => {
                infoWindow.open(this.map, marker);
            });

            this.markers.push(marker);
        });
    }
}

registry.category("actions").add("employee_gps_tracking.map", MapView);
