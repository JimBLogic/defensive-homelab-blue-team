# Defensive Homelab Blue Team Lab

This repository documents a Raspberry Pi Blue Team lab built around a Raspberry Pi 4 with 8GB RAM and SSD storage. It is a Docker-based monitoring and security operations portfolio project focused on Linux, network visibility, service health, metrics, logging, alerting, hardening, backups, incident response, and Bitcoin security lessons.

The project demonstrates practical junior SOC / Blue Team thinking through careful tool selection, sanitized architecture, repeatable review routines, and small operational exercises. It does not claim to reproduce an enterprise SOC.

## Why This Project Matters

Defensive work starts with understanding what should be running, what is exposed, which events are useful, and how failures are investigated and recovered. This repository documents those decisions before deployment and records how controls are validated over time.

## Blue Team Learning Goals

- Establish a clear host, container, service, and trust-boundary baseline.
- Monitor availability, Linux host health, container behavior, and DNS security events.
- Practice log review, metrics interpretation, alert triage, and incident documentation.
- Apply least privilege, local-only management access, and minimal service exposure.
- Validate backups and restores instead of assuming recovery will work.
- Translate Bitcoin and Lightning operations into privacy, availability, custody, and recovery lessons.

## Blue Team Tooling Direction

The lab evaluates open-source tools before installing them. Current first-phase candidates include:

- Uptime Kuma for service availability checks.
- Prometheus and Node Exporter for metrics and Linux host visibility.
- Grafana for operational dashboards.
- A carefully selected Docker/container monitoring approach.
- CrowdSec for future log-based detection and response practice.
- AdGuard Home for DNS filtering and privacy-aware DNS security review.
- Future IDS, log aggregation, and SIEM candidates for a later or external lab.

Selection considers Raspberry Pi resources, required privileges, data collection, exposure, maintenance, and portfolio value. See the [tool-selection rationale](blue-team-tools/tool-selection.md).

## Current Status

The documentation and privacy baseline is established. Tool-selection, architecture, hardening, monitoring, backup, and incident-response guidance are documented. Tools are candidates until an installation and validation exercise is completed and recorded.

The next operational exercise is a sanitized [Weekly Homelab Log Review](security/logging-and-monitoring.md#first-operational-exercise-candidate). Progress is tracked in the [roadmap](docs/roadmap.md).

## Repository Structure

| Area | Purpose |
| --- | --- |
| [`docs/`](docs/) | Project scope, architecture, hardware, network, roadmap, and lessons learned. |
| [`blue-team-tools/`](blue-team-tools/) | Tool selection and concise defensive evaluation pages. |
| [`docker/`](docker/) | Service review guidance and a placeholder-only Compose example. |
| [`security/`](security/) | Hardening, logging, backups, and incident response. |
| [`bitcoin-security/`](bitcoin-security/) | Sanitized Bitcoin, Lightning, and OPSEC lessons. |
| [`assets/diagrams/`](assets/diagrams/) | Future sanitized diagrams. |

### Key Documents

- [Architecture and trust boundaries](docs/architecture.md)
- [Blue Team tool selection](blue-team-tools/tool-selection.md)
- [Hardening checklist](security/hardening-checklist.md)
- [Logging and monitoring routine](security/logging-and-monitoring.md)
- [Backup and restore strategy](security/backup-strategy.md)
- [Incident response note template](security/incident-response-notes.md)
- [Roadmap](docs/roadmap.md)
- [Lessons learned](docs/lessons-learned.md)

## Privacy and Sanitization

This repository must not contain real public or private IP addresses, LAN details, hostnames, usernames, private domains, credentials, API keys, tokens, seed or recovery phrases, wallet data, VPN configuration, firewall rules, raw logs, or screenshots from the live environment.

Documentation uses placeholders such as `<HOMELAB_HOST>`, `<LAN_SUBNET>`, `<ADMIN_WORKSTATION>`, `<SERVICE_PORT>`, `<LOCAL_ONLY>`, `<VPN_ONLY>`, `<BACKUP_TARGET>`, and `<REDACTED>`. Real configuration and operational evidence remain outside the repository.

