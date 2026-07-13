# Project Overview

This repository documents a defensive homelab portfolio for practicing Linux administration, Docker operations, network monitoring, service health, log review, hardening, backups, and incident response thinking.

The goal is to show how a small Raspberry Pi lab can be planned, observed, secured, reviewed, and improved with a realistic Blue Team mindset.

## Scope

This project includes documentation for:

- Sanitized architecture, trust boundaries, and access categories.
- Lightweight open-source defensive tool selection.
- Linux host and Docker container visibility.
- Service availability, metrics, dashboards, and alerting concepts.
- DNS filtering and privacy-aware DNS security review.
- Host, SSH, container, and service hardening.
- Logging, backup verification, restore testing, and incident notes.
- Bitcoin and Lightning operational security lessons.

Tools are evaluated before deployment. Documentation does not imply that every candidate is installed or that the Raspberry Pi operates as a full enterprise SOC.

## Safety and Privacy Rules

This repository must not include:

- Real public or private IP addresses, subnets, hostnames, domains, or usernames.
- Credentials, secrets, recovery phrases, API keys, tokens, or wallet data.
- Real firewall rules, VPN configuration, raw logs, or production configuration.
- Screenshots or labels that identify the live environment.

Use placeholders such as `<HOMELAB_HOST>`, `<LAN_SUBNET>`, `<SERVICE_PORT>`, `<BACKUP_TARGET>`, and `<REDACTED>` when examples are needed.

## Portfolio Value

This project is intended to demonstrate:

- Risk-aware tool selection and resource planning.
- Secure architecture and minimal-exposure thinking.
- Metrics, log, and service-health review habits.
- Clear incident and recovery documentation.
- Honest progress tracking without overstating implementation.

## TODO

- [ ] Complete the first sanitized Weekly Homelab Log Review.
- [ ] Validate one lightweight monitoring tool at a time.
- [ ] Perform an isolated backup restore exercise.
- [ ] Record findings and improvements in `docs/lessons-learned.md`.
