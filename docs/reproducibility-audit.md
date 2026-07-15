# Reproducibility Audit

## Existing baseline preserved

The repository already contained a useful Raspberry Pi Docker baseline with Uptime Kuma, Prometheus, Node Exporter, Grafana provisioning, optional cAdvisor target discovery, AdGuard Home test documentation, and CrowdSec evaluation notes. The new foundation preserves the same core services, named volume names, localhost administrative bindings, Prometheus and Grafana configuration paths, and the detection-before-remediation stance.

## Changes made for reproducibility

- Replaced the single `deploy/docker-compose.yml` deployment entry with `deploy/compose.yaml`, `deploy/compose.lite.yaml`, and `deploy/compose.full.yaml`.
- Centralized explicit candidate image pins in `deploy/.env.example`.
- Added static validation that does not require a running Docker daemon.
- Documented LITE/FULL selection, migration safety, version verification status, and rollback cautions.

## Security assumptions

Dashboards remain loopback-only. Node Exporter and cAdvisor do not publish host ports. AdGuard Home uses localhost test DNS by default and does not replace LAN DNS. CrowdSec has no bouncer. Wazuh central services are not deployed on the Pi. Tailscale and future Wazuh agent work remain native host integration topics.
