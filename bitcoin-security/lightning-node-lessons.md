# Lightning Node Lessons

Lightning nodes introduce additional operational risk because availability, backups, and key management matter.

## Lessons

- Protect seed material, channel backups, macaroon files, and TLS keys.
- Understand backup limitations before opening channels.
- Monitor node uptime and channel health.
- Avoid exposing administrative interfaces.
- Keep operational notes sanitized and free of real peer or channel details.

## Defensive Takeaways

- Availability and security are connected.
- Recovery planning must be specific and tested.
- Secrets should be stored outside public repositories.

## TODO

- [ ] Add a sanitized backup and recovery checklist.
- [ ] Document monitoring requirements.
- [ ] Add lessons learned from maintenance events.
