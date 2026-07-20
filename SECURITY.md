# Security policy

## Public repository boundary

This repository contains sanitized documentation and reproducible examples. It must not contain live infrastructure evidence or access material, including:

- public or private IP addresses tied to the homelab;
- real hostnames, usernames, domains, LAN topology or firewall rules;
- `.env` files, credentials, API keys, tokens, VPN profiles or private keys;
- packet captures, raw logs, local databases, backups or screenshots;
- Bitcoin wallet data, descriptors, seed or recovery phrases;
- notification endpoints, webhook URLs or service session data.

The automated validator catches common patterns and risky tracked filenames, but it cannot prove that a commit is sanitized. Review every diff manually before publication.

## Reporting a vulnerability or exposure

Do not place sensitive evidence in a public issue. Use GitHub private vulnerability reporting when available, or contact the repository owner through the methods listed on the GitHub profile.

Include the affected revision, the exposure or impact, and safe reproduction details using placeholders.

## Accidental publication response

Deleting a secret or evidence file in a later commit does not remove it from Git history. Treat published material as compromised:

1. revoke or rotate affected credentials, tokens and certificates;
2. replace exposed VPN profiles, webhooks or service sessions;
3. assess whether hostnames, addresses, logs or packet data reveal additional attack paths;
4. remove the sensitive blobs from repository history and review forks, caches and artifacts;
5. inspect relevant service and authentication logs;
6. document the incident using sanitized identifiers only.

For Bitcoin-related material, assume any exposed seed phrase or private key is permanently compromised and migrate funds to a newly generated wallet using a reviewed recovery process.

## Supported scope

Security fixes target the current default branch. The Compose baseline is a learning environment and is not represented as an enterprise SOC or production-managed service.
