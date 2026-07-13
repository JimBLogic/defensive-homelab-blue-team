# Future Defensive Tools

## Purpose

Record tools that may add value after the lightweight baseline is stable, while explaining why they are not first-phase Raspberry Pi deployments.

## Why They May Fit Later

Advanced tools can teach log aggregation, packet analysis, detection engineering, and SIEM workflows. Their value depends on suitable hardware, network visibility, storage, and operational maturity.

## Candidate Classification

| Candidate | Category | Decision rationale |
| --- | --- | --- |
| Netdata | Optional / evaluate later | Rich visibility, but full collection can require host networking, capabilities, and sensitive mounts. |
| Loki with Promtail or Alloy | Optional / evaluate later | Useful aggregation after retention, labeling, and manual review processes are understood. |
| Suricata | Optional now; external lab candidate | Requires packet visibility, capture permissions, tuning, and performance capacity. |
| Zeek | External or x86 lab | Strong network metadata, but too complex and resource-intensive for the first Raspberry Pi phase. |
| Wazuh | External x86 stack or agent-only study | Full manager, indexer, and dashboard stack is too heavy for this host. |
| Security Onion | External x86 lab only | Not a Raspberry Pi deployment target. |

## Defensive Value

- Central log search and correlation.
- Network intrusion detection and protocol analysis.
- Alert triage, rule tuning, and case documentation.

## Data Collected

Depending on the tool: host logs, application logs, packet-derived metadata, IDS alerts, endpoint events, metrics, and case information.

## Security Considerations

- Evaluate required privileges, packet access, host mounts, agents, and management APIs.
- Plan storage, retention, updates, backup, and removal before deployment.
- Keep management interfaces isolated and prevent accidental packet or log overcollection.

## Privacy Considerations

Centralized logs and network telemetry may reveal addresses, domains, user behavior, payload context, and host details. External lab datasets should be synthetic, authorized, or thoroughly sanitized.

## Exposure Recommendation

Management interfaces remain `<LOCAL_ONLY>` or `<VPN_ONLY>`. External x86 lab systems require their own documented trust boundaries and must never be assumed safe by default.

## Example Use Cases

- Compare manual log review with a small Loki query in a later exercise.
- Analyze synthetic Suricata or Zeek data in an isolated external lab.
- Run a Wazuh agent-only learning exercise against an authorized test system.

## TODO / Future Improvements

- [ ] Define the learning question before selecting any advanced tool.
- [ ] Estimate CPU, memory, storage, privileges, and telemetry volume.
- [ ] Use synthetic or sanitized data for external lab exercises.
