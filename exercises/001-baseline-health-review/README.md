# 001 — Baseline Service Health Review

**Status: IN PROGRESS / NOT VERIFIED**

**Deployment-ready defensive baseline · operational validation in progress**

This is the next operational exercise, not a completed case study. Repository preparation and static checks have been performed; the editing environment has no Docker CLI/daemon, no local baseline endpoints and no live homelab access. No live service-health result is asserted.

## Detection

A scheduled manual baseline review will trigger this exercise. No security alert or SIEM detection has been observed.

## Evidence

Required live sources: local Docker Engine/Compose state, actual port bindings, healthchecks, Prometheus targets and host metrics, Grafana datasource health, Uptime Kuma monitor history, bounded container logs and private host/SSH boundary review. See [evidence summary](evidence-summary.md) and [commands](queries-or-commands.md). Raw evidence stays outside Git.

## Initial hypothesis

The deployed services should match the reviewed four-service baseline, with loopback management bindings and healthy telemetry. This is an untested hypothesis until the host review is performed.

## Analysis

Distinguish configured, running, healthy and useful telemetry. A running container or an HTTP 200 is insufficient for a working datasource or a configured Kuma monitor. Compare resource use and cumulative restart counts at two observations at least five minutes apart, explain recent maintenance and investigate any increase. Review filesystem headroom on the actual Docker and Prometheus storage, not just the checkout filesystem.

The collector checks automated observations and leaves explicit manual gaps. Do not enable cAdvisor or collect DNS histories for this review. Do not start or restart services merely to make a check pass.

## Timeline

| Date / context | Observation | Implication |
| --- | --- | --- |
| 2026-10-08 / repository audit | Source configuration and existing safeguards inspected. | This establishes a review procedure, not live deployment. |
| 2026-10-08 / editing environment | Docker unavailable; baseline loopback endpoints unavailable. | Live review remains NOT VERIFIED. |
| Pending / homelab host | Two collection times and manual review window. | Replace with actual sanitized facts after execution. |

## MITRE ATT&CK

**Not mapped.** Service-health checks do not demonstrate adversary behavior. No telemetry supports an ATT&CK technique here; confidence in any adversary mapping is insufficient. If a genuinely suspicious event is found, open a separate investigation and justify its mapping with the supporting evidence.

## Query

No live Docker or PromQL query has been executed against the homelab in this exercise. [The commands file](queries-or-commands.md) contains the exact proposed commands, PromQL and private UI checks.

## Classification

**Inconclusive — live operational review pending.** Once reviewed, use N/A — baseline health review if no security event exists. If there is a security event, classify the separate case using the common template.

## Impact

No live service impact was observed or measured. Potential blind spots: missing scrape targets, unconfigured monitors, failed datasource, crash loops, disk/log growth and unexpected exposure.

## Containment / Action

No live containment or deployment change performed. Repository-only action: gate optional profiles and document privilege exceptions. Unexpected broad exposure or privileged services require operator review before any corrective host action.

## Escalation decision

No event is available to close or escalate. During the review, investigate unexpected exposure, OOM/crash loops, stale/missing telemetry, unexplained restart increases, unknown project services or log errors. Escalate suspected compromise or secret exposure; do not assume a configuration fault explains it.

## L2 handoff

**Pending simulated handoff note.** Include sanitized finding, two collection times, expected/observed behavior, evidence IDs, affected service role, query results, actions actually taken, gaps and one concrete escalation question. No handoff has been sent.

## Lessons learned

[Current preparation lessons](lessons-learned.md) are source-review findings only. Live operation lessons remain pending.

## Detection tuning

None performed. Resource/restart/disk thresholds need an observed baseline and documented headroom rationale. Log keyword counts are triage hints, not detections.

## Sanitisation

Follow [the checklist](../SANITISATION.md). The collector uses allowlisted projections; publication still requires human review. Do not copy inspect/config/API output, host listener details, raw logs or sensitive screenshots.

## Run and close the exercise

1. On the authorized homelab host, confirm the local repository revision and the actually deployed LITE/FULL file set. Review [runtime exceptions](../../security/runtime-exceptions.md).
2. Run preflight, the lightweight verifier and the collector; [commands and exit meanings](queries-or-commands.md) explain incomplete results.
3. Collect again after at least five minutes of normal operation. Keep both files outside the checkout. Record actual times privately.
4. Privately check Kuma monitor configuration/history, bounded logs for all reviewed services, Grafana datasource health, storage location, SSH tunnel and host/firewall/user/capability boundaries.
5. Fill the summary with actual reviewed observations, finding IDs, actions, a timeline and gaps. A failed check can be part of a completed investigation if its cause/disposition is recorded; an unavailable core observation must not be marked passed.
6. Finish the lessons and simulated L2 note, run repository validation and manually review the staged diff. Only then mark COMPLETED and add the case to the root README's Operational evidence.

## Completion criteria

- [ ] Authorized homelab execution, mode, code revision and two collection times recorded.
- [ ] All expected containers accounted for; state, health and application readiness compared.
- [ ] Actual IPv4/IPv6 published bindings and host-network exceptions reviewed.
- [ ] Prometheus required targets are present, up and recently scraped; Node Exporter supplies host metrics.
- [ ] Grafana provisioned datasource configuration and connection health verified.
- [ ] At least one approved Kuma monitor is configured; interval, status and history inspected.
- [ ] CPU/memory, OOM state and restart-count delta reviewed over the stated window.
- [ ] Actual Docker/metrics storage free capacity and growth/retention rationale recorded.
- [ ] Rotation settings and bounded private logs reviewed; errors explained or investigated.
- [ ] SSH, host listeners/firewall, secret permissions, effective privileges and optional profiles reviewed.
- [ ] Findings, justified N/A items, classification, actions and simulated escalation/handoff recorded.
- [ ] Human sanitisation review and repository checks passed; no sensitive artifacts staged.
