# Roadmap

This roadmap tracks realistic progress from a documentation baseline toward a repeatable defensive operations portfolio. Checked items are represented in the repository; operational exercises remain unchecked until they are actually performed and documented safely.

## Phase 1: Documentation Foundation

- [x] Create the starter documentation structure.
- [x] Define project scope, portfolio purpose, and privacy rules.
- [x] Add sanitized hardware, network, security, Docker, service, and Bitcoin security pages.
- [x] Use placeholders instead of real infrastructure values.

## Phase 2: Architecture and Service Baseline

- [x] Document a sanitized logical architecture and trust boundaries.
- [x] Categorize local-only, VPN-only, and non-public management access.
- [x] Provide a placeholder-only Docker Compose example.
- [x] Frame self-hosted services as access-control, logging, update, and recovery practice.
- [ ] Create a sanitized inventory of service purpose, owner, image version, data, ports, and dependencies.
- [ ] Document an update, validation, and rollback routine for one service.

## Phase 3: Security Operations

- [x] Expand the host and Docker hardening checklist.
- [x] Define high-value log sources and a weekly review checklist.
- [x] Create a reusable incident response note template.
- [ ] Complete and document one sanitized weekly log review.
- [ ] Establish a normal baseline before defining alert thresholds.
- [ ] Perform a service exposure review and record remediation tasks.

## Phase 4: Backup and Recovery Validation

- [x] Document backup scope, exclusions, verification, and failure scenarios.
- [ ] Set recovery objectives, frequency, and retention using placeholders in public notes.
- [ ] Perform an isolated restore test for one service.
- [ ] Record sanitized evidence of backup integrity and restore validation.
- [ ] Add recurring storage-health and capacity checks.

## Phase 5: Bitcoin Security Lessons

- [x] Document starter Bitcoin node, Lightning node, and OPSEC lessons.
- [x] Separate portfolio documentation from wallet, key, channel, and recovery material.
- [ ] Add a sanitized node-failure scenario and defensive response notes.
- [ ] Record lessons from a recovery exercise without exposing financial or network data.
- [ ] Review how availability, backups, privacy, and key custody create different risks.

## Phase 6: Portfolio Polish

- [x] Improve README navigation and explain the Blue Team learning purpose.
- [x] Add a structured lessons-learned page for future evidence.
- [ ] Add a sanitized architecture diagram under `assets/diagrams/`.
- [ ] Cross-check service pages against the architecture and checklists.
- [ ] Run a final privacy, link, clarity, and overclaiming review.
- [ ] Publish only material that has passed the sanitization review.

