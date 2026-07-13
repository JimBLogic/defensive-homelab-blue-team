# Logging and Monitoring

Logging, metrics, health checks, and dashboards support a defensive learning cycle: establish a baseline, detect meaningful deviations, investigate with evidence, and document improvements.

## Monitoring Goals

- Detect authentication problems, service failures, container instability, resource pressure, and backup issues.
- Keep enough evidence to troubleshoot and build a reliable incident timeline.
- Distinguish container state, application health, and host health.
- Collect only data that supports a defined operational or security purpose.

## Visibility Sources

| Source | Useful events or data | Review focus |
| --- | --- | --- |
| Uptime Kuma | Check state, response time, outage duration, recovery | Repeated failures, dependency impact, and whether downtime meets incident criteria. |
| Prometheus | Time-series metrics, scrape success, resource trends | Missing targets, sustained threshold changes, and retention health. |
| Grafana | Dashboards and alert views | Clear context, accurate labels, and whether panels support a decision. |
| Node Exporter | CPU, memory, filesystem, network, and supported hardware metrics | Disk pressure, sustained resource use, temperature trends, and host degradation. |
| Docker logs and container state | Application errors, restarts, health, and exit behavior | Crash loops, new errors, or behavior after an update. |
| Container metrics exporter | Container CPU, memory, network, and restart trends | Unexpected resource spikes and noisy or unstable workloads. |
| Host and SSH logs | Service failures, logins, authentication failures, session activity | Repeated failures, unusual timing, or an unexpected `<REDACTED_SOURCE>`. |
| DNS security logs | Allowed and blocked requests, filter status, sanitized trends | Query spikes, repeated `<REDACTED_DOMAIN>` patterns, and false positives. |
| CrowdSec, if implemented | Alerts, decisions, scenarios, and bouncer results | Evidence quality, false positives, decision expiry, and enforcement impact. |
| Backup job logs | Job result, copied data, verification, capacity, and errors | Missed runs, incomplete copies, or integrity failures. |

Actual log locations and scrape targets remain private. Public examples must use placeholders and must not include real users, addresses, domains, DNS histories, or infrastructure labels.

## First Operational Exercise Candidate

The [deployment baseline](../deploy/README.md) defines Operational Exercise 001 â€” Baseline Service Health Review. It validates the four default containers, SSH-tunnel access, Prometheus scraping, Grafana connectivity, restart counts, and disk usage before more complex monitoring is added.

### Weekly Homelab Log Review

Start with a manual weekly review before adding complex alerting. Record the review date, sources checked, expected maintenance, sanitized findings, and follow-up actions.

- [ ] Review failed SSH login attempts and compare them with expected access.
- [ ] Review container restarts, health changes, and new application errors.
- [ ] Review Uptime Kuma service-health checks and any downtime.
- [ ] Review backup job status and verification results.
- [ ] Review a privacy-safe DNS security summary, not raw browsing history.
- [ ] Review Prometheus target health and important host metrics if implemented.
- [ ] Review CrowdSec alerts or decisions only if the tool has been validated.
- [ ] Record findings in `docs/lessons-learned.md`.
- [ ] Open an incident note if an event appears abnormal or requires containment.

## High-Value Events to Watch

- Multiple authentication failures followed by a success.
- A successful administrative login from an unexpected source or time.
- A new listening service, published port, user, authorized key, or privileged container.
- Repeated container restarts, missing scrape targets, failed health checks, or dashboard gaps.
- Sustained CPU, memory, temperature, filesystem, or network changes outside the baseline.
- DNS security spikes or repeated blocked activity that requires privacy-aware triage.
- CrowdSec decisions that could affect legitimate access.
- Backup jobs that stop, shrink unexpectedly, or fail verification.

## Fictional Sanitized Events

These examples are invented and are not copied from the live environment.

```text
<UTC_TIMESTAMP> <HOMELAB_HOST> sshd: authentication failure for <REDACTED> from <REDACTED_SOURCE>
<UTC_TIMESTAMP> <UPTIME_CHECK>: state changed from healthy to unavailable
<UTC_TIMESTAMP> <CONTAINER_NAME>: restart count exceeded <PLACEHOLDER_VALUE>
<UTC_TIMESTAMP> <BACKUP_JOB>: verification failed for <BACKUP_TARGET>
```

For each event, ask: Is it expected? What changed? Which independent source confirms it? What is the impact? Does it require an incident note, a tuning change, or only documentation?

## Data Minimization and Privacy

- Define the purpose and `<RETENTION_PERIOD>` for each log and metric source.
- Restrict access to dashboards, APIs, metrics endpoints, logs, and alert histories.
- Avoid exporting full DNS histories, client identifiers, real addresses, or authentication details.
- Sanitize dashboard labels and screenshots before any future publication.
- Use counts, trends, and redacted excerpts when documenting lessons.
- Delete data when its operational purpose and retention requirement have ended.

## SOC / Blue Team Learning Value

This routine practices source identification, baseline comparison, event correlation, alert triage, evidence handling, incident documentation, and control improvement. The goal is disciplined entry-level defensive practice, not an enterprise monitoring claim.

## TODO

- [ ] Complete the first Weekly Homelab Log Review.
- [ ] Define a small normal baseline before setting alert thresholds.
- [ ] Document check ownership, retention, and escalation criteria.
- [ ] Add tools one at a time and remove data sources that do not support a clear decision.
