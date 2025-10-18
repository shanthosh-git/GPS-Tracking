/** @odoo-module */

import { standardViewProps } from "@web/views/view";
import { Component, onWillStart, onWillUpdateProps, onWillUnmount, useRef } from "@odoo/owl";

// A promise that resolves when the Google Maps script is loaded
const googleMapsLoaded = new Promise((resolve) => {
    if (window.google && window.google.maps) {
        resolve();
    } else {
        const interval = setInterval(() => {
            if (window.google && window.google.maps) {
                clearInterval(interval);
                resolve();
            }
        }, 100);
    }
});

export class LiveMapRenderer extends Component {
    static template = "employee_gps_tracking.LiveMapView";
    static props = {
        ...standardViewProps,
        employees: { type: Array, element: Object },
    };

    setup() {
        this.root = useRef("map");
        this.map = null;
        this.markers = new Map();

        onWillStart(async () => {
            // Wait for the Google Maps script to be fully loaded before proceeding
            await googleMapsLoaded;
        });

        onWillUpdateProps((nextProps) => {
            this.updateMarkers(nextProps.employees);
        });

        onWillUnmount(() => {
            // Cleanup if needed
        });
    }

    onMounted() {
        this.initMap();
        this.updateMarkers(this.props.employees);
    }

    initMap() {
        if (this.map || !this.root.el) return;
        this.map = new google.maps.Map(this.root.el, {
            center: { lat: 0, lng: 0 },
            zoom: 2,
        });
    }

    updateMarkers(employees) {
        if (!this.map) return;

        const employeeIds = new Set();
        const bounds = new google.maps.LatLngBounds();

        for (const employee of employees) {
            employeeIds.add(employee.id);
            const position = { lat: employee.latest_latitude, lng: employee.latest_longitude };

            if (this.markers.has(employee.id)) {
                const marker = this.markers.get(employee.id);
                marker.setPosition(position);
            } else {
                const marker = new google.maps.marker.AdvancedMarkerElement({
                    position,
                    map: this.map,
                    title: employee.name,
                });
                this.markers.set(employee.id, marker);
            }
            bounds.extend(position);
        }

        for (const [id, marker] of this.markers.entries()) {
            if (!employeeIds.has(id)) {
                marker.map = null;
                this.markers.delete(id);
            }
        }

        if (employees.length > 0 && bounds.getNorthEast() && bounds.getSouthWest()) {
            this.map.fitBounds(bounds);
            if (employees.length === 1) {
                this.map.setZoom(15);
            }
        }
    }
}
