# Hardening Checklist

Use this checklist to review the homelab host and services from a defensive perspective.

## Host Hardening

- [ ] Apply operating system updates regularly.
- [ ] Disable unused services.
- [ ] Use strong, unique passwords or SSH keys.
- [ ] Disable password-based SSH login where appropriate.
- [ ] Restrict administrative access to trusted devices.
- [ ] Review user accounts and group membership.
- [ ] Enable firewall rules with a default-deny mindset.

## Docker Hardening

- [ ] Avoid privileged containers unless clearly justified.
- [ ] Use named volumes and documented bind mounts.
- [ ] Keep images updated from trusted sources.
- [ ] Avoid storing secrets in compose files.
- [ ] Limit published ports to only what is required.
- [ ] Review container logs after deployment and updates.

## TODO

- [ ] Add command examples using placeholders.
- [ ] Add service-specific hardening items.
- [ ] Schedule recurring checklist reviews.
