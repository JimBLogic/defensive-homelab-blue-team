# Incident Response Notes

This page provides a starter format for documenting security events and operational incidents in the homelab.

## Incident Note Template

| Field | Entry |
| --- | --- |
| Date/time | `<UTC_TIMESTAMP>` |
| Detection source | `<LOG_OR_ALERT_SOURCE>` |
| Summary | `<WHAT_HAPPENED>` |
| Impact | `<KNOWN_OR_SUSPECTED_IMPACT>` |
| Containment | `<ACTIONS_TAKEN>` |
| Evidence | `<SANITIZED_LOG_REFERENCES>` |
| Recovery | `<RECOVERY_STEPS>` |
| Lessons learned | `<FOLLOW_UP_ITEMS>` |

## Response Priorities

1. Stay calm and preserve useful evidence.
2. Disconnect or isolate affected services if needed.
3. Avoid destroying logs during cleanup.
4. Record actions taken and timestamps.
5. Review root cause after recovery.

## TODO

- [ ] Add sanitized example incident notes.
- [ ] Create a triage checklist for common events.
- [ ] Define when to rotate credentials.
