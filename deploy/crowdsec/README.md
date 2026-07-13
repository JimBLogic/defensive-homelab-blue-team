# CrowdSec Evaluation Notes

## Status

CrowdSec is documentation-only in this baseline. No Compose service, collection, remediation bouncer, or blocking action is enabled.

This deliberate pause keeps detection design ahead of enforcement. CrowdSec should be added only after approved log sources, data minimization, normal behavior, false-positive handling, and rollback are documented.

## Acquisition Example

`acquis.example.yaml` contains placeholders only. If a later evaluation is approved:

1. Select one authorized log source.
2. Copy the example to the ignored local file `acquis.yaml`.
3. Replace `<LOG_PATH>` and `<LOG_TYPE>` outside Git.
4. Confirm that collection is necessary and retention is limited.
5. Start in detection-only mode without a bouncer.

## Security and Privacy

- Logs may contain addresses, usernames, paths, and authentication events.
- Never mount broad log directories without reviewing their contents.
- Keep local APIs and enrollment credentials private.
- Review every alert against source evidence and expected maintenance.
- Document detections before considering blocking.
- Define decision expiry and recovery before any future bouncer.

## TODO

- [ ] Select and document one privacy-reviewed source.
- [ ] Establish a normal authentication baseline.
- [ ] Define sanitized alert fields and false-positive review.
- [ ] Propose a separate `detection` profile only after these tasks are complete.
