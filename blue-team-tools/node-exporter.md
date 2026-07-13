# Node Exporter

## Purpose

Expose Linux host metrics for CPU, memory, filesystem, network, load, and supported hardware collectors.

## Why It Fits This Homelab

Node Exporter provides direct visibility into Raspberry Pi host health and pairs naturally with Prometheus without requiring a large monitoring platform.

## Defensive Value

- Identifies resource pressure and storage risk.
- Supports host baselining and capacity review.
- Helps distinguish host problems from container problems.

## Data Collected

Host resource counters, filesystem information, network statistics, and supported sensor metrics such as CPU temperature where available.

## Security Considerations

- Restrict the metrics endpoint to the approved collector.
- Enable only collectors with a documented purpose.
- Review filesystem and label output for sensitive identifiers.
- Do not run with unnecessary privileges.

## Privacy Considerations

Metric labels can reveal device, interface, filesystem, or host details. Sanitize labels and never publish the raw endpoint.

## Exposure Recommendation

Metrics endpoint: not publicly exposed. Permit access only from the monitoring path on an internal Docker or host network.

## Example Use Cases

- Alert on low free space before backup or service failure.
- Compare CPU temperature with sustained workload.
- Record a sanitized weekly host-health baseline.

## TODO / Future Improvements

- [ ] Select required collectors only.
- [ ] Define disk, memory, load, and temperature review thresholds after baselining.
- [ ] Document how metric labels will be sanitized.
