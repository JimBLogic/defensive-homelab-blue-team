# Architecture

This document describes the defensive homelab at a level that is useful for review without revealing the real home network. All names, addresses, routes, and ports are represented by placeholders.

## Sanitized Architecture Diagram

```text
                         Internet
                            |
                    [Router / Firewall]
                            |
             no direct management exposure
                            |
                       <LAN_SUBNET>
                   _________|_________
                  |                   |
       <ADMIN_WORKSTATION>      <CLIENT_DEVICE>
                  |                   |
        local administration     local services
                  |                   |
                  +---- <HOMELAB_HOST> ----+
                         |                  |
                  [Docker networks]   [Host logging]
                    |     |     |           |
              DNS filter | self-hosted   health checks
                         management
                         interfaces
                              |
                       scheduled backups
                              |
                       <BACKUP_TARGET>

Remote administrator -> <VPN_ACCESS> -> <LAN_SUBNET>
                        (no direct public admin access)
```

The diagram shows intended access paths, not real routing or firewall configuration.

## Main Components

| Component | Role | Expected access | Defensive consideration |
| --- | --- | --- | --- |
| `<HOMELAB_HOST>` | Linux host for containers and security operations | Local administration or `<VPN_ACCESS>` | Keep the host patched and expose only required services. |
| Router/firewall | Boundary between the internet and `<LAN_SUBNET>` | Restricted administration | Management must not be exposed directly to the internet. |
| `<ADMIN_WORKSTATION>` | Approved system used for maintenance | Local or VPN-assisted | Protect administrative credentials and verify the destination before connecting. |
| Docker networks | Segmentation between service groups | Container-to-container as required | Do not publish internal databases or Docker management interfaces. |
| Self-hosted services | Practice targets for access control, updates, logs, and recovery | Usually local-only | Review authentication, ports, volumes, and logs per service. |
| Logging and health checks | Records security and availability events | Administrators only | Limit retention and avoid collecting unnecessary personal data. |
| `<BACKUP_TARGET>` | Separate recovery copy for critical data | Backup process and authorized administrators | Encrypt where appropriate and test restoration independently. |

## Trust Boundaries

1. **Internet to router/firewall:** traffic originating from the internet is untrusted. No homelab management interface should cross this boundary directly.
2. **Client devices to `<HOMELAB_HOST>`:** local presence does not imply full trust. Clients receive only the service access they require.
3. **Administrative access:** `<ADMIN_WORKSTATION>` and `<VPN_ACCESS>` form a higher-trust path that should use strong authentication and auditable logins.
4. **Host to containers:** containers are treated as isolated workloads, not as trusted extensions of the host. Permissions, mounts, capabilities, and networks remain limited.
5. **Primary storage to `<BACKUP_TARGET>`:** the backup boundary should reduce the chance that one mistake, compromise, or disk failure destroys both copies.

## Service Exposure Categories

| Category | Intended use | Examples |
| --- | --- | --- |
| Local-only | Available only to approved clients on `<LAN_SUBNET>` | User-facing self-hosted services and DNS filtering. |
| VPN-only for remote access | Reachable remotely only after an authenticated connection through `<VPN_ACCESS>` | SSH administration and management dashboards. |
| Not publicly exposed | Never intentionally reachable from the internet | Docker socket/API, database ports, internal metrics endpoints, backup repositories, and host management interfaces. |

Any exception requires a documented need, risk review, authentication plan, logging plan, and rollback path.

## Defensive Design Decisions

- Prefer local access and authenticated VPN access over public port forwarding.
- Publish the minimum number of container ports and avoid binding internal dependencies to every interface.
- Keep service data on documented persistent storage so containers can be rebuilt without losing required state.
- Separate routine user access from administrative access.
- Collect logs that support troubleshooting and detection while minimizing personal data.
- Keep secrets and environment-specific configuration outside version control.
- Treat backups and tested restores as part of service design, not as a later add-on.

## Security Assumptions

- The router/firewall is maintained and its administrative interface is not internet-facing.
- `<ADMIN_WORKSTATION>` and VPN credentials are protected, but local clients are not automatically trusted.
- The homelab is a learning environment, not a high-availability or enterprise security platform.
- Physical access, hardware failure, configuration mistakes, and compromised containers remain realistic risks.
- Repository documentation contains placeholders only and is not an authoritative copy of live configuration.

## Future Improvements

- [ ] Add a redacted diagram under `assets/diagrams/` that matches this logical view.
- [ ] Record each service's access category, owner, data, logs, and recovery priority.
- [ ] Document container network purposes without copying live values.
- [ ] Validate that management interfaces remain unreachable from untrusted networks.
- [ ] Review whether stronger network separation is practical for the available hardware.

