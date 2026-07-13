# Uptime Kuma Baseline Notes

## Role in the Default Stack

Uptime Kuma is the first availability-monitoring service in the baseline. Its dashboard binds to `127.0.0.1` and should be reached through an SSH tunnel from `<ADMIN_WORKSTATION>`.

## Initial Check

After creating a local administrator account, add one Docker-internal HTTP check for:

```text
http://prometheus:9090/-/ready
```

Use a sanitized name such as `<SERVICE_NAME>`. Define the expected result, check interval, and outage duration that would justify an incident note.

## Security and Privacy

- Keep the dashboard local-only or VPN-only.
- Store account and notification credentials outside Git.
- Monitor only authorized services.
- Do not publish real targets, notification URLs, contact details, or screenshots.
- Back up `uptime_kuma_data` before major updates.

## TODO

- [ ] Validate the first check through the Docker `monitoring` network.
- [ ] Record one controlled outage and recovery timeline.
- [ ] Define a small, approved service inventory before adding more checks.
