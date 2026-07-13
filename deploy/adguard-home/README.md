# AdGuard Home Optional Profile

## Status

AdGuard Home is disabled by default and runs only with the `dns` profile. It is included for careful DNS security testing, not as the automatic network resolver.

## Safe Test Model

- The administration interface binds to localhost using `${ADGUARD_ADMIN_PORT:-3002}`.
- TCP and UDP DNS listeners bind to localhost using `${ADGUARD_DNS_PORT:-5353}`.
- No LAN client is pointed to the service by this repository.
- Network-wide use requires a separate availability, port 53, privacy, and rollback review.

Start the profile only after reading the deployment guide:

```bash
docker compose --env-file .env --profile dns up -d
```

## Security and Privacy

- Protect the administrator account and configuration.
- Do not expose the dashboard or resolver publicly.
- DNS logs can reveal browsing behavior, client identity, and internal domains.
- Minimize retention and publish only redacted counts or trends.
- Do not commit DNS logs, blocklist exceptions, client labels, or real upstream configuration.

## TODO

- [ ] Validate local test resolution without changing client DNS settings.
- [ ] Define a privacy-safe retention period.
- [ ] Document false-positive review and rollback before broader use.
