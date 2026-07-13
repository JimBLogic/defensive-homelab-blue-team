# DNS Security

## Purpose

Use AdGuard Home as the single documented DNS filtering candidate for blocked-domain review, local resolver health, and privacy-aware DNS defense practice.

## Why It Fits This Homelab

AdGuard Home is appropriate for Raspberry Pi resources and makes DNS security, blocklist quality, false positives, service availability, and data minimization easy to explain.

## Defensive Value

- Reduces access to selected unwanted domains.
- Provides DNS health and sanitized trend visibility.
- Supports network-defense and false-positive review exercises.

## Data Collected

DNS request time, client information, requested domain, response, blocking decision, filter match, and service statistics depending on retention settings.

## Security Considerations

- Keep the administration interface `<LOCAL_ONLY>`.
- Protect configuration, credentials, and upstream settings.
- Review blocklist source, update, rollback, and availability impact.
- Monitor the resolver so filtering does not hide a broader service failure.

## Privacy Considerations

DNS history can reveal user behavior. Minimize retention, restrict access, avoid unnecessary client labels, and publish only counts or redacted trends such as `<REDACTED_DOMAIN>`.

## Exposure Recommendation

Administration: `<LOCAL_ONLY>`. DNS service reachability should be limited to approved clients on `<LAN_SUBNET>`. Do not expose the resolver or dashboard publicly.

## Example Use Cases

- Review a weekly count of blocked requests without publishing full queries.
- Investigate a false positive and record the safe rollback decision.
- Correlate resolver downtime with Uptime Kuma status.

## TODO / Future Improvements

- [ ] Define privacy-safe retention and reporting.
- [ ] Document approved blocklist review criteria.
- [ ] Create a false-positive handling exercise using placeholders.
