# Incident Response Notes

Use this template for security events and operational incidents. Preserve facts, distinguish observations from assumptions, and sanitize all entries before committing them to this repository.

## Reusable Incident Note Template

### Incident Title

`<SHORT_DESCRIPTIVE_TITLE>`

### Date/Time

- First observed: `<UTC_TIMESTAMP>`
- Incident window: `<START_TIME>` to `<END_TIME_OR_ONGOING>`
- Note updated: `<UTC_TIMESTAMP>`

### Detection Source

`<LOG_SOURCE_OR_HEALTH_CHECK>`

### Affected Service

`<SERVICE_NAME>` on `<HOMELAB_HOST>`

### Summary

Describe what was observed, the known impact, and the current status. Do not include real addresses, usernames, domains, credentials, or raw sensitive logs.

### Timeline

| Time | Observation or action | Result |
| --- | --- | --- |
| `<UTC_TIMESTAMP>` | `<OBSERVATION>` | `<RESULT>` |
| `<UTC_TIMESTAMP>` | `<ACTION_TAKEN>` | `<RESULT>` |

### Evidence Collected

- `<SANITIZED_LOG_REFERENCE>`
- `<CONFIGURATION_CHANGE_REFERENCE>`
- `<HEALTH_CHECK_RESULT>`

Record where original evidence is protected; include only redacted summaries here. Note the source, collection time, and relevant time zone.

### Suspected Cause

`<CONFIRMED_CAUSE_OR_WORKING_HYPOTHESIS>`

State the confidence level and what evidence would confirm or disprove the hypothesis.

### Containment Actions

- `<ACTION_TO_LIMIT_IMPACT>`
- `<ACCESS_OR_SERVICE_RESTRICTION>`

### Recovery Actions

- `<RESTORE_OR_REBUILD_STEP>`
- `<VALIDATION_STEP>`
- `<MONITORING_PERIOD>`

### Lessons Learned

- What control or process worked: `<OBSERVATION>`
- What made detection or recovery harder: `<OBSERVATION>`
- What should change: `<IMPROVEMENT>`

### Follow-Up Tasks

- [ ] `<OWNER_OR_ROLE>`: `<TASK>` by `<TARGET_DATE>`.
- [ ] Update the relevant checklist, service page, or recovery procedure.
- [ ] Confirm that committed notes remain sanitized.

## Fictional Sanitized Example

This example is invented and contains placeholders only.

### Incident Title

Repeated SSH authentication failures

### Date/Time

- First observed: `<UTC_TIMESTAMP>`
- Incident window: `<START_TIME>` to `<END_TIME>`

### Detection Source

Weekly review of `<SSH_AUTH_LOG>`

### Affected Service

SSH on `<HOMELAB_HOST>`

### Summary

Several failed authentication attempts from `<REDACTED_SOURCE>` were recorded. No unexpected successful login or service impact was found.

### Timeline

| Time | Observation or action | Result |
| --- | --- | --- |
| `<UTC_TIMESTAMP>` | Reviewer identified repeated failures. | Triage started. |
| `<UTC_TIMESTAMP>` | Successful logins and authorized maintenance were compared. | No unauthorized success identified. |
| `<UTC_TIMESTAMP>` | Access scope and SSH settings were reviewed. | Existing restriction to `<VPN_ACCESS>` confirmed. |

### Evidence Collected

- Count and time range from `<SSH_AUTH_LOG>`, with source and user fields redacted.
- Sanitized summary of the current SSH access policy.

### Suspected Cause

Rejected access attempts; intent remains unknown. Confidence is limited because the example contains no additional evidence.

### Containment Actions

- Confirmed that SSH was not directly exposed to the internet.
- Continued monitoring for a successful login or a change in pattern.

### Recovery Actions

No service recovery was required. Authentication and service-health checks passed.

### Lessons Learned

The review checklist made the pattern visible, while a documented normal baseline would make future triage faster.

### Follow-Up Tasks

- [ ] Define a review threshold for repeated SSH failures after observing normal activity.
- [ ] Recheck access restrictions during the next hardening review.

