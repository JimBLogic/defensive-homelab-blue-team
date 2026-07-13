# Jellyfin

Jellyfin is a self-hosted media server. In this portfolio, it is documented from an operational and defensive perspective.

## Defensive Questions

- Who can access the service?
- Is remote access required?
- How are user accounts managed?
- What logs are available?
- What data needs to be backed up?

## Security Considerations

- Prefer local-only access unless remote access is carefully designed.
- Use strong account passwords.
- Keep the container and host updated.
- Avoid documenting real library names, usernames, or media paths.

## TODO

- [ ] Add sanitized service configuration notes.
- [ ] Document backup requirements.
- [ ] Add update and rollback steps.
