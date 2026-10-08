# LITE vs FULL

| Mode | Intended host | Compose command | Services |
| --- | --- | --- | --- |
| LITE | Raspberry Pi 4 around 4 GB RAM | `docker compose --env-file .env -f compose.yaml -f compose.lite.yaml up -d` | Uptime Kuma, Prometheus, Node Exporter, Grafana OSS |
| FULL | Raspberry Pi 4 around 8 GB RAM with SSD | `docker compose --env-file .env -f compose.yaml -f compose.full.yaml up -d` | Same four core services with increased limits; optional profiles still off |

Resource limits are conservative guardrails, not performance guarantees. LITE keeps optional container and DNS telemetry disabled. Optional FULL profiles add more I/O and memory pressure, so measure actual use with `docker stats`, `free -h`, `df -h`, and Raspberry Pi temperature tooling.

Prometheus retention defaults to `7d` in `.env.example`; increasing it raises disk use. Docker JSON logs rotate at 10 MiB with three files per service. Disable FULL additions if the host shows sustained swap use, high temperature, storage pressure, or repeated container restarts.

Enable `--profile containers` or `--profile dns` only after the separate review in [runtime exceptions](../security/runtime-exceptions.md) and the deployment guide. cAdvisor is unnecessary for 001. Source/profile changes do not prove legacy containers stopped. No mode has live validation evidence yet.
