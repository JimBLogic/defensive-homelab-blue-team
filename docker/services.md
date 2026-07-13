# Docker Services

This document tracks planned Docker services and the defensive questions that should be answered before deployment.

## Service Review Template

| Question | Notes |
| --- | --- |
| What problem does the service solve? | `<SERVICE_PURPOSE>` |
| What data does it store? | `<DATA_TYPE>` |
| Does it need internet access? | `<YES_OR_NO>` |
| Does it need to be reachable from the internet? | Usually `No`. |
| What ports are required? | Use `<SERVICE_PORT>`. |
| How is authentication handled? | `<AUTH_METHOD>` |
| Where are logs stored? | `<LOG_LOCATION>` |
| How is it backed up? | `<BACKUP_METHOD>` |

## Planned Services

- AdGuard Home
- Jellyfin
- Jellyseerr
- Radarr
- Sonarr
- OpenVPN
- Monitoring tools
- Backup tooling
- Security logging tools

## TODO

- [ ] Add one reviewed entry per service.
- [ ] Document Docker networks and volumes.
- [ ] Add update procedure for containers.
- [ ] Add rollback notes for failed upgrades.
