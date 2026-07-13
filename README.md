# Raspberry Pi Defensive Homelab

This repository documents a practical defensive homelab built around a Raspberry Pi 4 with 8GB RAM and SSD storage. It uses Linux, Docker, networking, self-hosted services, monitoring, backups, hardening, and Bitcoin security lessons to demonstrate how a small environment can be operated and improved with a Blue Team mindset.

The project is a learning portfolio. It shows structured thinking, safe documentation, troubleshooting habits, and incremental improvement without claiming to reproduce an enterprise SOC.

## Why This Project Matters

Running a service is only the starting point. Defensive operations require knowing what is exposed, who can administer it, which logs support an investigation, how updates are validated, and whether recovery works after a mistake or hardware failure. This repository makes those decisions visible and reviewable.

Self-hosted media services are included only as infrastructure examples for practicing Docker operations, access control, updates, logging, backups, and exposure review.

## Blue Team Learning Goals

- Maintain a clear host, service, data, and trust-boundary baseline.
- Apply least privilege, secure access, and minimal exposure.
- Review authentication, system, container, DNS, VPN, backup, and health events.
- Practice evidence-based incident notes and follow-up actions.
- Plan and test recovery rather than assuming a backup is usable.
- Translate Bitcoin and Lightning operations into privacy, availability, custody, and recovery lessons.

## Current Status

The documentation foundation is complete. Sanitized architecture, hardening, monitoring, backup, and incident-response guidance is in place. The next stage is to perform small operational exercises—such as a weekly log review, service exposure review, and isolated restore test—and record only sanitized results.

Progress is tracked in the [roadmap](docs/roadmap.md).

## Repository Structure

| Area | Purpose |
| --- | --- |
| [`docs/`](docs/) | Project overview, architecture, hardware, network, goals, roadmap, and lessons learned. |
| [`docker/`](docker/) | Service planning and a placeholder-only Compose example. |
| [`security/`](security/) | Hardening, logging, backups, and incident response. |
| [`bitcoin-security/`](bitcoin-security/) | Sanitized Bitcoin, Lightning, and OPSEC lessons. |
| [`media-stack/`](media-stack/) | Infrastructure and security operations notes for self-hosted services. |
| [`assets/diagrams/`](assets/diagrams/) | Future sanitized diagrams. |

### Key Documents

- [Architecture and trust boundaries](docs/architecture.md)
- [Hardening checklist](security/hardening-checklist.md)
- [Logging and monitoring routine](security/logging-and-monitoring.md)
- [Backup and restore strategy](security/backup-strategy.md)
- [Incident response note template](security/incident-response-notes.md)
- [Roadmap](docs/roadmap.md)
- [Lessons learned](docs/lessons-learned.md)

The [project overview](docs/project-overview.md), [network layout](docs/network-layout.md), [security goals](docs/security-goals.md), and service-specific pages provide supporting context.

## Privacy and Sanitization

This repository must not contain real public or private IP addresses, LAN details, hostnames, usernames, domains, credentials, API keys, tokens, seed or recovery phrases, wallet data, VPN configuration, firewall rules, raw logs, or screenshots from the live environment.

Documentation uses placeholders such as `<HOMELAB_HOST>`, `<LAN_SUBNET>`, `<ADMIN_WORKSTATION>`, `<SERVICE_PORT>`, `<BACKUP_TARGET>`, `<VPN_ACCESS>`, and `<REDACTED>`. Sensitive operational configuration and evidence remain outside the repository.

