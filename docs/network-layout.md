# Network Layout

This document provides a safe, sanitized description of the homelab network layout.

## Privacy Notice

Do not commit real IP addresses, router details, MAC addresses, private hostnames, ISP information, VPN endpoints, or screenshots of network tools.

## Placeholder Layout

| Zone | Example Placeholder | Purpose |
| --- | --- | --- |
| LAN | `<LAN_SUBNET>` | Trusted home network segment. |
| Homelab host | `<HOMELAB_HOST>` | Runs Docker services. |
| Client devices | `<CLIENT_DEVICE>` | Devices using local services. |
| VPN users | `<VPN_CLIENT>` | Remote access if enabled. |
| Backup target | `<BACKUP_TARGET>` | Destination for backup copies. |

## Access Rules

- Admin panels should be local-only unless a documented secure access path is required.
- Remote access should use VPN or another strongly authenticated method.
- Default-deny thinking should guide firewall rules.
- Service ports should be documented with placeholders, not real exposed values.

## TODO

- [ ] Add a sanitized network diagram.
- [ ] Document intended firewall rules using placeholders.
- [ ] Identify services that should never be internet-facing.
- [ ] Add a review checklist for new service exposure.
