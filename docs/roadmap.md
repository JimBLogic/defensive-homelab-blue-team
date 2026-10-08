# Roadmap

**Deployment-ready defensive baseline · operational validation in progress**

Checked items mean files or controls exist in the repository. No live deployment or investigation is marked completed without dated, sanitized operational evidence.

## Completed repository preparation

- [x] Document privacy boundaries, architecture, logging, backups and hardening.
- [x] Provide the four-service LITE/FULL configuration and candidate image tags.
- [x] Require explicit optional-service profiles and document privilege exceptions.
- [x] Provide the consistent investigation template and Exercise 001 collection procedure.
- [x] Define completion criteria for planned exercises 002–005.
- [x] Choose one initial SIEM route: Windows / Sysmon → external Wazuh.

## Operate the current baseline first

- [ ] Verify selected image availability / ARM64 compatibility on the actual host.
- [ ] Run [001](../exercises/001-baseline-health-review/README.md): service health, telemetry, actual exposure, resource/restart comparison, disk, logs and security boundaries.
- [ ] Publish reviewed live findings and lessons; then link the completed case in Operational evidence.
- [ ] Repeat a bounded review and investigate a real health/restart finding if one occurs.
- [ ] Perform an isolated backup restore; restore planning is not tested recovery.
- [ ] Reduce effective capabilities/users only after compatibility tests and a reviewed exception decision.

## First SOC investigations

Follow the [telemetry roadmap](siem-telemetry-roadmap.md), with resource/isolation gates before deployment.

- [ ] [002 — Authentication triage](../exercises/002-authentication-triage/README.md).
- [ ] [003 — Process / PowerShell investigation](../exercises/003-process-or-powershell-investigation/README.md).
- [ ] [004 — Network / DNS investigation](../exercises/004-network-dns-investigation/README.md).
- [ ] [005 — Detection-rule tuning](../exercises/005-detection-rule-tuning/README.md).
- [ ] Learn basic KQL on an explicitly synthetic dataset after one real Wazuh query/investigation; no second SIEM is required.
- [ ] Practice EDR concepts and a simulated L2 handoff; do not claim professional incident ownership.

## Deferred; no installation queue

cAdvisor, AdGuard Home, CrowdSec, log aggregation and IDS tools require a specific unanswered learning question, privacy review, resource headroom and rollback. cAdvisor stays disabled for 001. Alternative SIEMs, Security Onion and packet-analysis stacks are deferred; do not deploy them simultaneously or add tools to make the portfolio look larger.
