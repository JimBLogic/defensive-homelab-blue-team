# Uptime Kuma

## Purpose

Provide service availability checks, response-time history, and a simple introduction to alerting and downtime documentation.

## Why It Fits This Homelab

Uptime Kuma is lightweight, understandable, and useful before a larger metrics stack. It supports a small first exercise without pretending that uptime alone proves security.

## Defensive Value

- Establishes expected service availability.
- Makes outages and recoveries visible.
- Encourages clear incident and escalation criteria.

## Data Collected

Check names, target labels, status, response time, outage duration, and optional notification history. Real targets and labels must remain private.

## Security Considerations

- Protect the dashboard with strong authentication.
- Limit checks to authorized targets.
- Keep notification credentials and URLs outside Git.
- Back up configuration before significant changes.

## Privacy Considerations

Use sanitized labels such as `<SERVICE_NAME>`. Do not publish real addresses, hostnames, domains, or notification content.

## Exposure Recommendation

Dashboard: `<LOCAL_ONLY>`. Use `<VPN_ONLY>` only when remote review is justified. Never expose it directly to the internet.

## Example Use Cases

- Record when `<SERVICE_NAME>` becomes unavailable and recovers.
- Compare downtime with container restart and host-health evidence.
- Decide whether an outage requires an incident note.

## TODO / Future Improvements

- [ ] Define a small approved check inventory.
- [ ] Define downtime severity and escalation criteria.
- [ ] Perform one fictional or controlled outage exercise.
