# Logging and Monitoring

Logging and monitoring turn normal homelab operations into a defensive learning cycle: establish a baseline, identify meaningful deviations, investigate with evidence, and document improvements.

## Monitoring Goals

- Detect authentication problems, service failures, unexpected changes, and backup issues.
- Keep enough evidence to troubleshoot and build a reliable incident timeline.
- Review service health without assuming that a running container is a healthy service.
- Collect only the data needed for a defined operational or security purpose.

## Log Sources

| Source | Useful events | Review focus |
| --- | --- | --- |
| SSH authentication logs | Successful logins, failures, invalid users, session start and end | Repeated failures, access outside expected periods, or an unexpected source such as `<REDACTED_SOURCE>`. |
| Docker container logs | Restarts, application errors, authentication failures, dependency problems | Crash loops, new error patterns, or behavior after an image update. |
| System update logs | Package changes, failed updates, reboot requirements | Missed security updates, unexpected package changes, or recurring failures. |
| DNS filtering logs | Allowed and blocked requests, filter status, client trends | Sudden query spikes or repeated requests to an unexpected `<REDACTED_DOMAIN>`. |
| VPN connection logs | Connection attempts, authentication results, session start and end | Repeated failures, unusual timing, or a new `<REDACTED_SOURCE>`. |
| Backup job logs | Job start and end, copied data, verification result, errors | Missed runs, incomplete copies, capacity problems, or verification failures. |
| Service health checks | Availability, response status, restart count, resource pressure | Repeated outages, degraded response, or a check that stops reporting. |

Document actual log locations privately. Public examples should use labels such as `<LOG_SOURCE>` and must not copy real usernames, addresses, domains, or queries.

## Weekly Log Review Checklist

- [ ] Confirm the host time and expected log sources are reporting.
- [ ] Review SSH and VPN successes and failures for unusual timing or repetition.
- [ ] Check container restarts, health-check failures, and new application errors.
- [ ] Confirm system updates completed or record why they were deferred.
- [ ] Look for DNS filtering spikes or repeated unusual patterns without recording personal browsing history.
- [ ] Verify scheduled backup jobs completed and their validation step passed.
- [ ] Compare high-value events with recent authorized maintenance.
- [ ] Record findings, false positives, and follow-up actions using sanitized notes.

## High-Value Events to Watch

- Multiple authentication failures followed by a success.
- A successful administrative login from an unexpected source or at an unusual time.
- A new listening service, published port, user, authorized key, or privileged container.
- Repeated container restarts, out-of-memory events, disk errors, or low free space.
- Security updates that repeatedly fail or a service that remains on an unsupported version.
- Backup jobs that stop running, shrink unexpectedly, or fail verification.
- Logging or health checks that become silent without an approved change.

## Fictional Sanitized Events

The following examples are invented to demonstrate triage questions. They are not copied from the live environment.

```text
<UTC_TIMESTAMP> <HOMELAB_HOST> sshd: authentication failure for <REDACTED_USER> from <REDACTED_SOURCE>
<UTC_TIMESTAMP> <SERVICE_NAME>: health check changed from healthy to unhealthy
<UTC_TIMESTAMP> <BACKUP_JOB>: verification failed for <BACKUP_TARGET>
<UTC_TIMESTAMP> <VPN_SERVICE>: repeated rejected connection from <REDACTED_SOURCE>
```

For each event, ask: Is it expected? What changed? What other evidence confirms it? What is the impact? Does it require containment, recovery, or only documentation?

## Data Minimization and Privacy

- Define a purpose and retention period for each log source.
- Restrict access to logs and protect them as operational data.
- Avoid exporting full DNS histories, client identifiers, real addresses, or authentication details to this repository.
- Use counts, trends, and redacted excerpts when documenting lessons.
- Delete logs when their operational purpose and retention requirement have ended.
- Never collect extra personal data merely because a service makes it available.

## SOC / Blue Team Learning Value

This routine practices skills used in entry-level defensive roles: identifying log sources, distinguishing normal activity from anomalies, correlating events across systems, preserving a timeline, documenting evidence, and turning findings into better controls. The goal is disciplined analysis, not claiming that a small homelab reproduces a full SOC.

## TODO

- [ ] Define `<RETENTION_PERIOD>` for each log source.
- [ ] Establish a sanitized baseline for normal service restarts and authentication activity.
- [ ] Complete one weekly review and record lessons without including raw personal data.
- [ ] Define alert thresholds only after observing normal behavior.

