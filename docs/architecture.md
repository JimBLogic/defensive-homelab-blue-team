# Architecture

This document describes the Defensive Homelab Blue Team Lab without revealing the real home network. Names, addresses, routes, ports, and configuration values are represented by placeholders.

## Sanitized Architecture Diagram

```text
                         Internet
                            |
                    [Router / Firewall]
                            |
                 no public dashboards
                            |
                       <LAN_SUBNET>
                  _________|_________
                 |                   |
      <ADMIN_WORKSTATION>       approved clients
                 |
        <LOCAL_ONLY> or <VPN_ONLY>
                 |
          +-- <HOMELAB_HOST> ----------------------+
          |       Linux + Docker Engine             |
          |                                          |
          |  Monitoring network                      |
          |  + Uptime checks                         |
          |  + Prometheus metrics                    |
          |  + Grafana dashboards                    |
          |                                          |
          |  Visibility sources                      |
          |  + Node Exporter host metrics            |
          |  + container metrics and restart status  |
          |  + host, SSH, Docker, and backup logs    |
          |                                          |
          |  Defensive services                      |
          |  + DNS security                          |
          |  + log-based detection if validated      |
          +-------------------|----------------------+
                              |
                     scheduled verified backups
                              |
                       <BACKUP_TARGET>
```

The diagram is a logical design, not a copy of live routing, Docker networks, or firewall rules.

## Main Components

| Component | Role | Expected access | Defensive consideration |
| --- | --- | --- | --- |
| `<HOMELAB_HOST>` | Linux and Docker platform | `<LOCAL_ONLY>` administration or `<VPN_ONLY>` | Patch the host and expose only reviewed services. |
| `<ADMIN_WORKSTATION>` | Approved maintenance and review system | Administrative path only | Protect credentials and verify the target before connecting. |
| Uptime monitoring | Records availability and check failures | Dashboard `<LOCAL_ONLY>` | Define what failure becomes an incident. |
| Prometheus and exporters | Collect host and container metrics | Metrics endpoints not public | Limit targets, labels, and retention. |
| Grafana | Presents operational dashboards | `<LOCAL_ONLY>` or `<VPN_ONLY>` | Sanitize labels and any future screenshots. |
| DNS security | Filters and summarizes DNS activity | Admin interface `<LOCAL_ONLY>` | Minimize retention and redact client and query details. |
| Log sources | Provide SSH, host, Docker, detection, and backup evidence | Administrators only | Protect logs and collect only what has a purpose. |
| `<BACKUP_TARGET>` | Holds separate recovery copies | Backup process and authorized administrators | Verify integrity and test isolated restores. |

## Trust Boundaries

1. **Internet to router/firewall:** internet traffic is untrusted. No dashboard or management interface should cross this boundary directly.
2. **Client network to monitoring services:** local presence does not create administrative trust. Dashboards and metrics endpoints remain restricted.
3. **Administrative access:** `<ADMIN_WORKSTATION>` uses `<LOCAL_ONLY>` access or an authenticated `<VPN_ONLY>` path.
4. **Host to containers:** containers are untrusted workloads with limited mounts, capabilities, ports, and network access.
5. **Docker control plane:** the Docker socket or API can provide host-level control and must not be exposed casually to monitoring containers.
6. **Primary storage to `<BACKUP_TARGET>`:** a separate recovery boundary reduces the impact of disk failure, deletion, or compromise.

## Exposure Categories

| Category | Intended use | Examples |
| --- | --- | --- |
| `<LOCAL_ONLY>` | Approved access from `<LAN_SUBNET>` | Uptime, Grafana, DNS administration, and review interfaces. |
| `<VPN_ONLY>` | Remote administration after authenticated VPN access | SSH and selected dashboards when remote review is justified. |
| Not publicly exposed | No intentional internet reachability | Docker socket/API, exporter endpoints, Prometheus API, internal logs, and backup storage. |

## Defensive Design Decisions

- Select and document tools before installation; do not deploy the full candidate list at once.
- Start with lightweight availability checks, then add metrics and dashboards in measured stages.
- Keep every management dashboard local-only or VPN-only.
- Avoid Docker socket access where possible; if a tool requires it, document the risk and use the narrowest read-only approach available.
- Sanitize DNS logs, metric labels, alerts, and dashboard images before publication.
- Keep secrets, real configuration, and production evidence outside version control.
- Treat backup verification and restore testing as monitoring outcomes.

## Security Assumptions

- The router/firewall is maintained and its management interface is not internet-facing.
- The lab is a learning environment with limited Raspberry Pi resources, not a high-availability SOC platform.
- Local clients are not automatically trusted, and administrative access remains restricted.
- Monitoring creates sensitive operational data that requires access control and retention limits.
- Real configurations are intentionally excluded from this repository.

## Future Improvements

- [ ] Validate the architecture against one first-phase deployment at a time.
- [ ] Document sanitized scrape targets, check ownership, and data retention decisions.
- [ ] Test that dashboards and metrics endpoints are unreachable from untrusted networks.
- [ ] Add a sanitized diagram under `assets/diagrams/` after the logical design is validated.
- [ ] Reassess advanced IDS or SIEM tooling in a better-suited external lab.

