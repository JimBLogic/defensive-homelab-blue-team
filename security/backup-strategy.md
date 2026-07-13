# Backup Strategy

Backups are a recovery control for mistakes, failed updates, hardware loss, and service misconfiguration. A backup is not considered dependable until its contents can be verified and restored.

## Backup Goals

- Rebuild `<HOMELAB_HOST>` without relying on the original disk.
- Restore critical service configuration and persistent data in a documented order.
- Keep at least one protected copy separate from primary storage.
- Use placeholders for recovery objectives: `<RECOVERY_POINT_OBJECTIVE>` and `<RECOVERY_TIME_OBJECTIVE>`.
- Avoid treating GitHub as storage for runtime data, archives, or secrets.

## What Should Be Backed Up

| Data | Example location | Frequency | Recovery priority |
| --- | --- | --- | --- |
| Sanitized deployment definitions | `<CONFIG_SOURCE>` | On approved change | High |
| Service configuration | `<SERVICE_CONFIG_PATH>` | `<BACKUP_FREQUENCY>` | High |
| Required persistent service data | `<SERVICE_DATA_PATH>` | `<BACKUP_FREQUENCY>` | Based on service impact |
| Host recovery notes and package inventory | `<RECOVERY_NOTES_PATH>` | After material change | Medium |
| Security and incident notes | `<SECURITY_NOTES_PATH>` | On approved change | Medium |
| Verification metadata | `<BACKUP_METADATA_PATH>` | Every backup run | High |

Caches, replaceable images, and easily regenerated data should be excluded when doing so reduces backup size and recovery complexity. Each service page should state what is required for a clean rebuild.

## What Must Not Be Committed to GitHub

- Passwords, API keys, tokens, private keys, VPN material, or real environment files.
- Seed phrases, recovery phrases, wallet files, channel backup data, or other financial secrets.
- Database dumps, service data, backup archives, or unredacted configuration.
- Real paths, hostnames, addresses, domains, usernames, logs, or screenshots that reveal the environment.

Sensitive material that genuinely requires backup belongs in a separate, access-controlled and appropriately encrypted process. This repository should contain only sanitized procedures and examples.

## Backup Schedule

| Backup class | Placeholder schedule | Destination | Retention |
| --- | --- | --- | --- |
| Critical configuration | `<CONFIG_BACKUP_FREQUENCY>` | `<BACKUP_TARGET>` | `<CONFIG_RETENTION>` |
| Persistent service data | `<DATA_BACKUP_FREQUENCY>` | `<BACKUP_TARGET>` | `<DATA_RETENTION>` |
| Offline or separate copy | `<SEPARATE_COPY_FREQUENCY>` | `<SEPARATE_BACKUP_TARGET>` | `<SEPARATE_COPY_RETENTION>` |
| Restore exercise | `<RESTORE_TEST_FREQUENCY>` | `<TEST_RESTORE_TARGET>` | Sanitized test record |

The schedule should reflect how much data loss is acceptable, how quickly a service must return, available storage, and the consequences of a failed backup window.

## Restore Testing Plan

1. Choose one service and define the expected restore result.
2. Prepare an isolated `<TEST_RESTORE_TARGET>` that cannot overwrite production data.
3. Select a known backup and verify its integrity before restoration.
4. Restore configuration and data in the documented dependency order.
5. Start the service without exposing it publicly and run functional checks.
6. Compare the result with the expected configuration and record gaps using sanitized notes.
7. Remove test data safely and update the recovery procedure.

## Backup Verification Checklist

- [ ] The scheduled job ran at `<EXPECTED_TIME>` and reported a clear result.
- [ ] The destination is reachable, protected, and has sufficient free space.
- [ ] Expected files are present and obvious temporary data is excluded.
- [ ] Integrity or checksum verification completed successfully.
- [ ] A separate copy is not dependent on the primary disk remaining healthy.
- [ ] Access to backup data is limited to the intended process and administrators.
- [ ] The latest restore test met `<RECOVERY_POINT_OBJECTIVE>` and `<RECOVERY_TIME_OBJECTIVE>` or produced a follow-up task.
- [ ] Documentation contains no real values or secret material.

## Failure Scenarios

| Scenario | Expected preparation | Recovery focus |
| --- | --- | --- |
| Primary SSD failure | Separate backup, replacement media, recovery notes | Rebuild the host and restore services by priority. |
| Corrupted or incomplete backup | Multiple restore points and verification results | Select a known-good copy and investigate the failed job. |
| Failed update or configuration change | Pre-change backup and rollback notes | Restore only the affected configuration or service data. |
| Accidental deletion | Retention that preserves earlier versions | Recover the smallest required data set. |
| Host compromise | Protected backup and trusted rebuild source | Do not restore unreviewed compromised configuration blindly. |
| Loss of `<BACKUP_TARGET>` | Separate or offline copy | Re-establish backup coverage before accepting further risk. |

## Storage and Disk Failure Lessons

- A second folder on the same SSD is not protection from SSD failure.
- Successful job output does not prove that the copied data is complete or restorable.
- Free-space exhaustion and filesystem errors can silently reduce backup reliability if they are not monitored.
- Backing up every cache and generated file increases recovery time and hides what is truly critical.
- Recovery order matters when services depend on networks, databases, identity, or shared storage.
- Simple, rehearsed restoration steps are more useful than an elaborate process that has never been tested.

## TODO

- [ ] Complete the per-service data inventory using sanitized labels.
- [ ] Set frequency and retention values from recovery requirements.
- [ ] Perform one isolated restore test and record the outcome.
- [ ] Add storage-health and backup-failure checks to the weekly review.

