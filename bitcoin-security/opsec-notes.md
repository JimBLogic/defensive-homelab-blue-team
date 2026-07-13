# OPSEC Notes

Operational security is especially important when documenting systems related to Bitcoin, Lightning, and home infrastructure.

## Repository OPSEC Rules

- Do not commit seed phrases, private keys, wallet files, macaroon files, TLS keys, API tokens, or credentials.
- Do not commit real node aliases, peer details, channel IDs, or private hostnames.
- Do not include screenshots that reveal balances, addresses, network details, or account names.
- Use placeholders for all sensitive values.

## Documentation Habits

- Write lessons learned without exposing private infrastructure.
- Redact logs before adding examples.
- Prefer conceptual diagrams over screenshots.
- Review commits for secrets before pushing.

## TODO

- [ ] Add a pre-publish privacy review checklist.
- [ ] Add safe examples of redacted logs.
- [ ] Document secret scanning tools to evaluate.
