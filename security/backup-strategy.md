# Backup Strategy

Backups are a core defensive control. The goal is to recover from mistakes, hardware failure, and service misconfiguration.

## Backup Principles

- Back up configuration and important service data.
- Keep at least one backup copy separate from the primary host.
- Test restores on a schedule.
- Protect backups from unauthorized access.
- Do not commit backup archives or real backup paths to this repository.

## Backup Planning Table

| Data | Frequency | Destination | Restore Notes |
| --- | --- | --- | --- |
| Service configs | `<FREQUENCY>` | `<BACKUP_TARGET>` | `<RESTORE_STEPS>` |
| Docker compose files | `<FREQUENCY>` | `<BACKUP_TARGET>` | `<RESTORE_STEPS>` |
| Documentation | On change | Git repository | Clone repository. |

## TODO

- [ ] Identify critical data per service.
- [ ] Document restore testing procedure.
- [ ] Add backup verification checklist.
- [ ] Define retention periods.
