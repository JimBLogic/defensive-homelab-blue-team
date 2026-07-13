# Logging and Monitoring

Logging and monitoring help turn the homelab into a defensive learning environment.

## Goals

- Understand normal service behavior.
- Identify failed logins, errors, crashes, and unusual activity.
- Keep enough logs to support troubleshooting and incident notes.
- Avoid collecting unnecessary personal or sensitive data.

## Log Sources

| Source | Example Events |
| --- | --- |
| Host logs | SSH logins, service failures, updates. |
| Docker logs | Container restarts, application errors. |
| DNS filtering | Blocked domains and client trends using sanitized notes. |
| VPN logs | Connection attempts and authentication failures. |
| Backup logs | Successful and failed backup jobs. |

## TODO

- [ ] Define log retention goals.
- [ ] Document where logs are stored.
- [ ] Add a weekly log review checklist.
- [ ] Add alerting ideas for high-value events.
