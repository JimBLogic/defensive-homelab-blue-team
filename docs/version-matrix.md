# Version Matrix

Image variables are centralized in `deploy/.env.example` and copied into local `deploy/.env` for deployment. These are explicit candidate pins supplied by the project research; none use `latest`, broad major tags, RC, beta, alpha, edge, or development tags.

| Component | Variable | Image tag | Manifest status |
| --- | --- | --- | --- |
| Uptime Kuma | `UPTIME_KUMA_IMAGE` | `louislam/uptime-kuma:2.4.0-slim` | Pending on-device verification. |
| Prometheus | `PROMETHEUS_IMAGE` | `prom/prometheus:v3.13.1` | Pending on-device verification. |
| Node Exporter | `NODE_EXPORTER_IMAGE` | `prom/node-exporter:v1.12.1` | Pending on-device verification. |
| Grafana | `GRAFANA_IMAGE` | `grafana/grafana:13.1.0` | Pending on-device verification. |
| cAdvisor | `CADVISOR_IMAGE` | `google/cadvisor:v0.60.5` | Pending on-device verification. |
| AdGuard Home | `ADGUARD_HOME_IMAGE` | `adguard/adguardhome:v0.107.76` | Pending on-device verification. |
| CrowdSec | `CROWDSEC_IMAGE` | `crowdsecurity/crowdsec:1.7.8-debian` | Pending on-device verification. |

## Verification note

This Codex environment did not have Docker Engine or Docker Compose, and a one-time registry API attempt returned `403 Forbidden`. Therefore ARM64 manifests were not confirmed here. On the Raspberry Pi, run:

```bash
cd deploy
./scripts/validate-repository.sh
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config
docker compose --env-file .env -f compose.yaml -f compose.full.yaml config
```

Then inspect/pull images on the Pi before deployment. Do not claim runtime compatibility until the selected mode has been tested on the actual Raspberry Pi 4.
