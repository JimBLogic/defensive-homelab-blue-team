# OpenVPN

OpenVPN can provide remote administrative access when configured carefully.

## Defensive Value

- Reduces need to expose individual services directly to the internet.
- Supports authenticated access to internal resources.
- Provides useful logs for connection review.

## Security Considerations

- Protect certificates, keys, and client profiles.
- Revoke access for lost or retired devices.
- Keep VPN software updated.
- Do not commit real VPN configuration files, public endpoints, or client names.

## TODO

- [ ] Document sanitized access model.
- [ ] Add certificate lifecycle notes.
- [ ] Add VPN log review checklist.
