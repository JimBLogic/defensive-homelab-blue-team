# Architecture

This document describes the high-level design of the defensive homelab using sanitized placeholders only.

## Design Principles

- Keep the environment simple enough to understand and maintain.
- Prefer defensive visibility over unnecessary complexity.
- Avoid exposing services to the internet unless there is a documented need.
- Separate documentation, configuration examples, and sensitive local values.
- Use repeatable deployment patterns where possible.

## High-Level Components

| Component | Purpose | Notes |
| --- | --- | --- |
| Homelab host | Runs Docker services and security tooling | Use `<HOSTNAME>` as a placeholder. |
| Router/firewall | Controls local network access | Do not document real admin URLs or IPs. |
| Docker network | Isolates service traffic where practical | Use named Docker networks. |
| Storage | Holds service data and backups | Document recovery steps separately. |
| Admin workstation | Used for maintenance | Avoid storing secrets in the repository. |

## Trust Boundaries

- Local user devices are treated as less trusted than the homelab host.
- Internet-facing access should be avoided or tightly controlled.
- Admin interfaces should require strong authentication.
- Backups should be protected from accidental deletion and ransomware-style impact.

## Data Flow Placeholder

```text
<ADMIN_WORKSTATION> -> <HOMELAB_HOST> -> Docker services
<CLIENT_DEVICE> -> DNS filtering -> Internet
<MONITORING_TOOL> -> Logs and service health checks
<BACKUP_TARGET> <- Scheduled backups from <HOMELAB_HOST>
```

## TODO

- [ ] Add a sanitized diagram under `assets/diagrams/`.
- [ ] Document each Docker network and its purpose.
- [ ] Identify which services require local-only access.
- [ ] Add notes on authentication and authorization boundaries.
