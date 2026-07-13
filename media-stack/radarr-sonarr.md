# Radarr and Sonarr

Radarr and Sonarr automate media management workflows. They should be documented carefully because they commonly integrate with other services.

## Defensive Questions

- Which integrations are required?
- Where are API keys stored?
- Which folders are mounted into containers?
- What permissions do the containers need?

## Security Considerations

- Never commit API keys, indexer details, credentials, or private paths.
- Use least-privilege file permissions.
- Avoid exposing the web interfaces outside the trusted network.
- Review logs after updates or integration changes.

## TODO

- [ ] Add sanitized volume and permission plan.
- [ ] Document integration security expectations.
- [ ] Add backup and restore notes.
