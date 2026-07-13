# Docker Services

This document tracks defensive tool candidates and the questions that must be answered before deployment. Inclusion here means evaluation or planning, not installation.

The first testable default stack and setup instructions are available in [`deploy/`](../deploy/README.md). Optional profiles remain subject to the reviews documented below.

## Service Review Template

| Question | Notes |
| --- | --- |
| What defensive problem does the tool address? | `<SERVICE_PURPOSE>` |
| What host, container, log, metric, or DNS data does it collect? | `<DATA_TYPE>` |
| What privileges, capabilities, mounts, or socket access does it require? | `<REQUIRED_ACCESS>` |
| Does it need internet access? | `<YES_OR_NO>` |
| What interface or `<SERVICE_PORT>` is exposed? | `<LOCAL_ONLY>` or `<VPN_ONLY>` |
| How is administrative access protected? | `<AUTH_METHOD>` |
| What is the retention and deletion plan? | `<RETENTION_PLAN>` |
| What should be backed up and how is restore tested? | `<BACKUP_METHOD>` |
| How will updates and rollback be validated? | `<UPDATE_AND_ROLLBACK>` |

## Candidate Services

| Candidate | Role | Planning status |
| --- | --- | --- |
| Uptime Kuma | Service availability and basic alerting | Recommended first operational tool. |
| Prometheus | Metrics collection and retention | Plan after availability monitoring. |
| Grafana | Dashboards and operational communication | Pair with an approved metrics source. |
| Node Exporter | Linux host metrics | Limit endpoint exposure. |
| Container metrics exporter | Docker resource and restart visibility | Evaluate privilege and socket risk first. |
| CrowdSec | Log-based detection and response concepts | Add only after a log baseline exists. |
| AdGuard Home | DNS filtering and security summaries | Local-only administration; privacy review required. |
| Backup tooling | Verified recovery jobs and status | Select from recovery requirements. |

See [Blue Team tool selection](../blue-team-tools/tool-selection.md) for the staged rationale.

## TODO

- [ ] Complete one review template before enabling each candidate.
- [ ] Document Docker networks, volumes, and exposure using placeholders.
- [ ] Validate one service at a time and record rollback steps.
- [ ] Remove candidates that do not justify their privileges or maintenance cost.
