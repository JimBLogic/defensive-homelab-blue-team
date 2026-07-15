# LITE vs FULL

| Mode | Intended host | Compose command | Services |
| --- | --- | --- | --- |
| LITE | Raspberry Pi 4 around 4 GB RAM | `docker compose --env-file .env -f compose.yaml -f compose.lite.yaml up -d` | Uptime Kuma, Prometheus, Node Exporter, Grafana OSS |
| FULL | Raspberry Pi 4 around 8 GB RAM with SSD | `docker compose --env-file .env -f compose.yaml -f compose.full.yaml up -d` | LITE plus cAdvisor and AdGuard Home test mode |

Resource limits are conservative guardrails, not performance guarantees. LITE keeps optional container and DNS telemetry disabled. FULL adds more I/O and memory pressure, so measure actual use with `docker stats`, `free -h`, `df -h`, and Raspberry Pi temperature tooling.

Prometheus retention defaults to `7d` in `.env.example`; increasing it raises disk use. Docker JSON logs rotate at 10 MiB with three files per service. Disable FULL additions if the host shows sustained swap use, high temperature, storage pressure, or repeated container restarts.
