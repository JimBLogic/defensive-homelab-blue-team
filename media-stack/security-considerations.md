# Media Stack Security Considerations

Media services are useful for learning Docker operations, but they should still be treated as part of the homelab attack surface.

## Common Risks

- Exposed web interfaces.
- Weak or reused passwords.
- Overly broad volume mounts.
- Unmanaged API keys and integration tokens.
- Outdated containers.
- Logs containing private usernames, paths, or activity.

## Defensive Practices

- Keep services local-only unless remote access is required and documented.
- Use VPN for remote administration where practical.
- Store secrets outside version control.
- Review container permissions and published ports.
- Back up configuration before major changes.
- Sanitize logs before adding them to documentation.

## TODO

- [ ] Create a per-service risk table.
- [ ] Add a recurring media stack review checklist.
- [ ] Document safe update process.
