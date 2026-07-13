# Blue Team Tool Selection

This document evaluates open-source defensive tools for a Raspberry Pi 4 with 8GB RAM running Docker. Selection is based on defensive value, resource cost, required privileges, data sensitivity, operational complexity, and the ability to produce honest portfolio evidence.

The list is a decision record, not an installation plan. Each tool should be reviewed, deployed, and validated separately.

A minimal first baseline is now prepared under [`deploy/`](../deploy/README.md). Only Uptime Kuma, Prometheus, Node Exporter, and Grafana start by default; cAdvisor and AdGuard Home require explicit profiles, and CrowdSec remains documentation-only.

## Selection Principles

- Prefer one clear learning objective per deployment.
- Start with lightweight visibility before adding aggregation or automated response.
- Keep dashboards, APIs, exporters, and administration interfaces `<LOCAL_ONLY>` or `<VPN_ONLY>`.
- Reject tools whose privileges, maintenance, or data collection are not justified.
- Define retention, backup, rollback, and removal before collecting operational data.
- Record sanitized outcomes rather than claiming tools are active before validation.

## 1. Recommended First-Phase Tools

| Tool | Primary role | Why it fits | First portfolio evidence |
| --- | --- | --- | --- |
| [Uptime Kuma](uptime-kuma.md) | Availability checks | Lightweight and useful for a first operational exercise | Document one check, outage criteria, and sanitized downtime note. |
| [Prometheus](prometheus.md) | Metrics collection | Widely used foundation for infrastructure visibility | Define approved scrape targets and retention. |
| [Grafana](grafana.md) | Dashboards | Turns metrics into clear operational views | Design a sanitized host-health dashboard. |
| [Node Exporter](node-exporter.md) | Linux host metrics | Directly supports Raspberry Pi health review | Establish a CPU, memory, filesystem, and temperature baseline. |
| [Container monitoring](docker-container-monitoring.md) | Docker visibility | Connects container operations with abnormal-behavior review | Compare restart count, health, CPU, and memory trends. |
| [CrowdSec](crowdsec.md) | Log-based detection | Supports authentication triage, decisions, and false-positive learning | Evaluate sanitized SSH detections after a log baseline exists. |
| [AdGuard Home](dns-security.md) | DNS security | Provides filtering and privacy-aware network defense practice | Review a sanitized blocked-query summary and false positives. |

### Suggested Order

1. Validate Uptime Kuma with a small approved check list.
2. Add Node Exporter and Prometheus for host metrics.
3. Add Grafana only after useful metrics and labels are defined.
4. Evaluate a least-privilege container metrics source.
5. Document and validate DNS security reporting.
6. Evaluate CrowdSec after normal authentication and log patterns are understood.

## 2. Optional / Evaluate Later

| Tool | Value | Reason to delay |
| --- | --- | --- |
| Netdata | Rich real-time host visibility | Full visibility may require host networking, capabilities, and sensitive mounts. |
| Loki with Promtail or Alloy | Central log aggregation | Adds storage, retention, labeling, and troubleshooting complexity. |
| Suricata | Network intrusion detection | Requires suitable packet visibility, capture permissions, tuning, and performance testing. |

## 3. Too Heavy or Not Ideal for Raspberry Pi

| Tool | Assessment |
| --- | --- |
| Zeek | Valuable network security monitoring, but packet analysis and data volume are too complex for the first Raspberry Pi phase. |
| Full Wazuh stack | Strong SIEM/XDR learning value, but manager, indexer, and dashboard components are not a realistic first deployment on this host. |

## 4. Future External Lab / x86 Lab Candidates

- Suricata with controlled network visibility and dedicated capture resources.
- Zeek for network metadata and protocol-analysis exercises.
- Wazuh as an external x86 stack, with an agent-only learning path considered separately.
- Security Onion on supported external x86 resources only.
- Loki with Promtail or Alloy when basic review and retention processes are stable.

See [Future Tools](future-tools.md) for the decision questions that must be answered before expanding the lab.

## TODO

- [ ] Complete a resource and privilege review before each deployment.
- [ ] Record an explicit success condition and rollback plan for the first tool.
- [ ] Update status only after validation and sanitized evidence are complete.
