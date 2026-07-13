# CrowdSec

## Purpose

Evaluate log-based behavior detection, alerts, decisions, and controlled blocking concepts for approved services such as SSH.

## Why It Fits This Homelab

CrowdSec provides practical Blue Team learning around parsing, scenarios, false positives, decision lifecycles, and the difference between detection and enforcement.

## Defensive Value

- Detects repeated suspicious behavior in supported logs.
- Encourages evidence review before automated action.
- Supports authentication and exposure-hardening lessons.

## Data Collected

Selected log events, parsed metadata, alerts, scenario matches, decisions, and optional bouncer results. Exact sources depend on the approved collection plan.

## Security Considerations

- Start with observation before enabling a bouncer.
- Restrict the local API and protect enrollment or integration credentials.
- Review collections and scenarios before activation.
- Define decision expiry, rollback, and false-positive handling.

## Privacy Considerations

Logs and alerts may contain source addresses, usernames, paths, or domains. Store only what is required and publish redacted summaries.

## Exposure Recommendation

API and dashboard access: `<LOCAL_ONLY>`. Administrative access may use `<VPN_ONLY>` when justified. No public management endpoint.

## Example Use Cases

- Review a fictional SSH brute-force alert using `<REDACTED_SOURCE>`.
- Compare an alert with raw host evidence and authorized maintenance.
- Document why a decision should expire or be reversed.

## TODO / Future Improvements

- [ ] Establish a normal SSH and service log baseline first.
- [ ] Evaluate one collection without enforcement.
- [ ] Define false-positive review and bouncer rollback steps.
