# Hardening Checklist

This checklist supports repeatable reviews of the host and its services. For Blue Team learning, the value is not simply checking boxes: each item encourages a clear baseline, an observable control, and a reasoned response when the environment changes.

## Host Hardening

- [ ] Apply supported operating system updates on a documented schedule.
- [ ] Remove or disable packages and services that are not required.
- [ ] Verify time synchronization so event timelines remain useful.
- [ ] Review disk space, storage health, and failed system services.
- [ ] Confirm sensitive configuration files have restrictive ownership and permissions.

## SSH Access

- [ ] Use keys or another strong authentication method for administrative access.
- [ ] Disable password authentication when recovery needs and compatibility permit.
- [ ] Prevent direct remote login to the highest-privilege account.
- [ ] Limit SSH access to `<ADMIN_WORKSTATION>`, `<LAN_SUBNET>`, or `<VPN_ACCESS>` as appropriate.
- [ ] Review successful and failed SSH authentication events.

## User and Permission Review

- [ ] Remove unused accounts and stale authorized keys.
- [ ] Grant administrative privileges only where required.
- [ ] Check group membership and service-account access.
- [ ] Use least-privilege permissions for service files and persistent data.

## Firewall Mindset

- [ ] Start from deny-by-default thinking for unsolicited inbound traffic.
- [ ] Allow only documented services from documented trust zones.
- [ ] Keep management interfaces off the public internet.
- [ ] Review firewall intent after every new service or access change.
- [ ] Document examples with placeholders rather than copying live rules.

## Docker Hardening

- [ ] Avoid privileged mode, host networking, and unnecessary Linux capabilities.
- [ ] Do not mount the Docker socket unless the risk is understood and justified.
- [ ] Use read-only filesystems and non-root container users where supported.
- [ ] Limit bind mounts to the data each service requires.
- [ ] Separate workloads with named networks when this reduces unnecessary access.
- [ ] Define restart and health-check behavior deliberately.

## Container Image Hygiene

- [ ] Use maintained images from trusted publishers.
- [ ] Pin versions or digests where controlled upgrades are more important than automatic change.
- [ ] Review release notes and image provenance before updating.
- [ ] Remove unused images after confirming rollback requirements.
- [ ] Record the image version in sanitized service documentation.

## Secrets Handling

- [ ] Keep passwords, API keys, tokens, private keys, seed phrases, and recovery material out of Git.
- [ ] Use protected runtime secret files or a suitable secrets mechanism.
- [ ] Restrict secret-file permissions and avoid exposing values in process arguments or logs.
- [ ] Rotate a secret if accidental disclosure is suspected.
- [ ] Commit only example files containing values such as `<PLACEHOLDER_VALUE>`.

## Exposed Ports

- [ ] Inventory every published `<SERVICE_PORT>` and its purpose.
- [ ] Bind services to the narrowest appropriate interface.
- [ ] Confirm internal databases, metrics, and management ports are not publicly exposed.
- [ ] Remove obsolete port mappings after service changes.
- [ ] Test exposure from an untrusted perspective using only authorized methods.

## Update Process

- [ ] Back up critical configuration and data before significant changes.
- [ ] Review upstream security notices and release notes.
- [ ] Update one logical service group at a time when practical.
- [ ] Verify service health, authentication, and logs after updating.
- [ ] Keep a tested rollback or recovery path.

## Service Review

- [ ] Confirm the service still has a clear purpose and owner.
- [ ] Review authentication, permissions, dependencies, data, logs, and backup coverage.
- [ ] Disable default accounts, sample content, and unused features where applicable.
- [ ] Remove abandoned containers, volumes, networks, and scheduled tasks carefully.

## Physical and Hardware Considerations

- [ ] Restrict casual physical access to the host and backup media.
- [ ] Use a suitable power supply and prefer graceful shutdowns.
- [ ] Monitor SSD health, temperature, free space, and filesystem errors.
- [ ] Keep recovery media and sanitized recovery notes available.
- [ ] Store any offline backup separately from the primary host.

## Review Notes

Record the review date as `<REVIEW_DATE>`, the reviewer as `<REDACTED>`, exceptions as `<DOCUMENTED_EXCEPTION>`, and follow-up work in the [roadmap](../docs/roadmap.md). Revisit this checklist after major deployments, incidents, and architecture changes.

