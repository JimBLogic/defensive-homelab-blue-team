# Prometheus

## Purpose

Collect time-series metrics from approved targets and provide a foundation for infrastructure monitoring and alerting concepts.

## Why It Fits This Homelab

Prometheus is widely used, works well with Linux and container exporters, and teaches scraping, labels, retention, target health, and query-based investigation.

## Defensive Value

- Establishes normal resource and service patterns.
- Reveals missing targets and sustained changes.
- Supports evidence-based threshold decisions.

## Data Collected

Approved host, container, and service metrics with timestamps and labels. Scrape targets, labels, and retention values remain sanitized in repository examples.

## Security Considerations

- Do not expose the API or metrics database publicly.
- Restrict scrape targets and network paths.
- Avoid secrets in configuration, labels, or command arguments.
- Monitor storage growth and failed scrapes.

## Privacy Considerations

Collect only metrics tied to a documented question. Avoid labels containing real hostnames, usernames, domains, or client identifiers.

## Exposure Recommendation

Prometheus API: `<LOCAL_ONLY>`. Exporter endpoints should be reachable only from the approved metrics collector path.

## Example Use Cases

- Detect low disk space or sustained memory pressure on `<HOMELAB_HOST>`.
- Identify a scrape target that stops reporting.
- Compare resource trends with a service-health failure.

## TODO / Future Improvements

- [ ] Define approved `<SCRAPE_TARGET>` entries.
- [ ] Set `<RETENTION_PERIOD>` from storage and investigation needs.
- [ ] Document a small baseline before creating alerts.
