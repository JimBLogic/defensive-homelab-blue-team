# Defensive Homelab Blue Team

**Deployment-ready defensive baseline · operational validation in progress**

A small Raspberry Pi 4 / Docker learning lab for service-health review, Linux telemetry, hardening and evidence-based incident triage. The target is demonstrable Junior SOC / Blue Team practice. **No completed live operational exercise is published yet.**

| Recruiter question | Inspectable answer |
| --- | --- |
| What is this? | A reproducible defensive monitoring baseline for a Raspberry Pi 4 with SSD storage. |
| What is running? | **Not verified on the homelab.** The default configuration defines Uptime Kuma, Prometheus, Node Exporter and Grafana. Configuration is not proof of deployment. |
| What have I actually operated? | No live operation is evidenced in this repository yet. Exercise 001 has an executable review procedure and remains **IN PROGRESS / NOT VERIFIED**. |
| What security decisions did I make? | Loopback dashboard bindings, an internal metrics network, rotating logs, explicit image tags, excluded secrets, bounded resources, and disabled optional profiles. Privilege exceptions are documented. |
| What evidence can I inspect? | Source configuration and automated repository checks today; sanitized operational reports only after real execution and human review. |
| What is still planned? | Windows / Sysmon telemetry, one external Wazuh learning environment, queries, alert triage, an incident note and detection tuning. Exercises 002–005 are **PLANNED**. |

## Operational evidence

**None published yet.** This section will link only to exercises actually performed on the authorized lab, with dated, sanitized findings and unresolved checks stated explicitly. Templates, synthetic tests and CI checks do not count as live operational evidence.

## Exercise queue

| Exercise | Status | Deliverable |
| --- | --- | --- |
| [001 — Baseline Service Health Review](exercises/001-baseline-health-review/README.md) | IN PROGRESS / NOT VERIFIED | Read-only collection, manual review, findings and security-boundary validation. |
| [002 — Authentication triage](exercises/002-authentication-triage/README.md) | PLANNED | Correlate failed and successful logons with approved test activity. |
| [003 — Process / PowerShell investigation](exercises/003-process-or-powershell-investigation/README.md) | PLANNED | Reconstruct a process tree and justify classification. |
| [004 — Network / DNS investigation](exercises/004-network-dns-investigation/README.md) | PLANNED | Correlate controlled DNS / network telemetry with a process. |
| [005 — Detection-rule tuning](exercises/005-detection-rule-tuning/README.md) | PLANNED | Compare a rule before and after a narrow, tested change. |

All investigations use the [same case template](exercises/_investigation-template.md). ATT&CK mappings require observed behavior, supporting telemetry and stated confidence; a service-health review normally has no ATT&CK mapping.

## Baseline and security decisions

- **LITE** supplies the four core services with conservative resource limits. **FULL** increases limits; cAdvisor (`containers`), AdGuard Home (`dns`) and CrowdSec (`detection`) still require explicit profiles and prior review.
- Dashboards bind to `127.0.0.1`; Node Exporter and cAdvisor publish no host ports. SSH forwarding is the documented administrative path. These declarations still need runtime and host/firewall verification.
- `no-new-privileges`, explicit version tags and JSON log rotation are retained. Tags are candidate pins, not immutable digests or proof of ARM64 compatibility.
- cAdvisor's privileged mode and host mounts are a high-risk exception. A read-only `/var/run` mount can expose the Docker socket. It stays disabled for Exercise 001; Docker's native status and resource commands are sufficient.
- Node Exporter's host PID namespace and read-only host root are also an explicit exception. [Runtime exceptions and stop conditions](security/runtime-exceptions.md) explain both decisions.
- Real configuration, credentials, raw logs, DNS histories, packet captures and screenshots stay private. Only reviewed, minimized summaries belong here.

## Run the next review

Follow the [deployment guide](deploy/README.md), then run this **on the authorized homelab host** using the same mode as the deployed stack:

```bash
cd deploy
./scripts/preflight-check.sh lite
./scripts/verify-stack.sh lite
python3 scripts/baseline-health-review.py --mode lite --output /tmp/baseline-health-review.json
```

The collector does not start, stop, install or reconfigure services. It projects known fields into a sanitized report, refuses output inside the checkout, suppresses raw errors and never auto-completes an exercise. Exit code `2` means incomplete/manual checks; `1` means a failed check. Review the report and the private UI/logs, then finish [001's completion criteria](exercises/001-baseline-health-review/README.md).

## Repository checks and learning path

```bash
./deploy/scripts/validate-repository.sh
python3 -m unittest discover -s tests -v
```

Compose rendering requires Docker Compose; use `REQUIRE_COMPOSE=1` to fail if it is unavailable. [Validation record](docs/validation-2026-10-08.md) separates repository checks from unverified deployment. [SIEM / telemetry roadmap](docs/siem-telemetry-roadmap.md) defines one initial Windows + Sysmon → external Wazuh path. Other platforms remain deferred.

## Reference documents

- [Architecture and trust boundaries](docs/architecture.md)
- [Deployment and safe profile activation](deploy/README.md)
- [LITE vs FULL](docs/lite-vs-full.md) · [candidate image pins](docs/version-matrix.md)
- [Roadmap](docs/roadmap.md) · [lessons learned](docs/lessons-learned.md)
- [Hardening](security/hardening-checklist.md) · [logging](security/logging-and-monitoring.md) · [backups and restore](security/backup-strategy.md)
- [Tool-selection rationale](blue-team-tools/tool-selection.md) · [Bitcoin / Lightning privacy lessons](bitcoin-security/opsec-notes.md)
- [Evidence handling and sanitisation](exercises/SANITISATION.md) · [security policy](SECURITY.md)

**Build less. Operate more. Evidence > architecture diagrams.**
