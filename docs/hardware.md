# Hardware

This page documents the intended hardware profile for the homelab without exposing sensitive environment details.

## Baseline Hardware

| Item | Role | Notes |
| --- | --- | --- |
| Raspberry Pi 4 | Primary homelab host | 8GB RAM target platform. |
| SSD storage | Persistent service data | Use encrypted or access-controlled storage where practical. |
| Power supply | Stable power | Use a reliable power adapter suitable for the device. |
| Network connection | LAN connectivity | Prefer wired Ethernet for reliability. |

## Operational Considerations

- Monitor storage health and free disk space.
- Keep the host physically secure.
- Use graceful shutdown procedures when possible.
- Keep spare boot media and recovery notes available.
- Label cables and devices without exposing private names in public documentation.

## TODO

- [ ] Add sanitized hardware inventory details.
- [ ] Document storage layout using placeholders.
- [ ] Add maintenance schedule for updates and disk health checks.
- [ ] Document recovery process for failed storage media.
