# Grafana

## Purpose

Present approved metrics in dashboards that support operational review, investigation, and clear communication.

## Why It Fits This Homelab

Grafana pairs with Prometheus and helps turn raw metrics into understandable host, container, and service-health views.

## Defensive Value

- Brings related signals into a shared view.
- Supports baseline comparison and triage.
- Practices communicating technical status without exposing sensitive context.

## Data Collected

Grafana stores dashboard definitions, data-source references, users, preferences, and optional alert history. The source metrics remain in the configured data source.

## Security Considerations

- Change default credentials and restrict administrative roles.
- Protect data-source credentials outside version control.
- Review plugins and updates before installation.
- Back up dashboard definitions using sanitized exports only.

## Privacy Considerations

Dashboard titles, labels, annotations, and screenshots may reveal infrastructure. Replace real values with `<REDACTED>` before publication.

## Exposure Recommendation

Dashboard: `<LOCAL_ONLY>` by default, or `<VPN_ONLY>` for justified remote administration. Never directly internet-facing.

## Example Use Cases

- Build a host-health view for CPU, memory, filesystem, and temperature.
- Correlate service downtime with host and container metrics.
- Prepare a sanitized incident timeline panel.

## TODO / Future Improvements

- [ ] Define a minimum useful dashboard before adding more panels.
- [ ] Document role and data-source access.
- [ ] Create a screenshot sanitization checklist before sharing images.
