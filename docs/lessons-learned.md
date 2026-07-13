# Lessons Learned

This page provides a consistent place to record practical learning as the homelab evolves. Entries should describe what was observed, why it matters defensively, and what will change next. Keep all examples sanitized.

## Portfolio Progress Log — Defensive Homelab

Completed PR #2: `Improve defensive homelab documentation depth`.

This update improved the Raspberry Pi Defensive Homelab repository by adding deeper Blue Team documentation around sanitized architecture, trust boundaries, service exposure categories, hardening routines, logging and monitoring, backup verification, restore planning, incident response notes, and a realistic six-phase roadmap.

The repository now better represents a practical junior SOC / Blue Team portfolio project focused on Linux, Docker, networking, defensive operations, documentation, backups, logs, and Bitcoin security lessons.

Next step: complete one real but sanitized operational exercise, ideally a weekly log review, and record the result in `docs/lessons-learned.md`.

## Tooling Direction Change

The repository is moving from broad application-hosting documentation toward a focused open-source Blue Team lab. The updated direction prioritizes service availability, host and container metrics, dashboards, DNS security, log-based detection, backup validation, and SOC-style operational notes.

This change keeps the Raspberry Pi scope realistic: tools are selected and documented before deployment, lightweight controls come first, and advanced IDS or SIEM platforms are reserved for a more suitable external lab. Future entries should record what was tested, what evidence was reviewed, and how the result improved the defensive baseline.

## Entry Format

- **Context:** `<SANITIZED_ACTIVITY_OR_CHANGE>`
- **Observation:** `<WHAT_HAPPENED>`
- **Defensive relevance:** `<WHY_IT_MATTERS>`
- **Improvement:** `<NEXT_ACTION>`
- **Validation:** `<HOW_THE_CHANGE_WILL_BE_CHECKED>`

## Linux Administration Lessons

- Record lessons about updates, services, permissions, storage, resource use, and troubleshooting.
- TODO: Document one issue identified through host logs and the verified corrective action.

## Docker Operations Lessons

- Record lessons about images, networks, volumes, health checks, updates, and rollback.
- TODO: Compare container status with application-level health for one sanitized example.

## Backup and Storage Lessons

- Record lessons from backup verification, restore exercises, disk health, capacity, and failure planning.
- TODO: Add the result of an isolated restore test without including real paths or data.

## Logging and Monitoring Lessons

- Record useful log sources, baseline behavior, false positives, retention decisions, and detection improvements.
- TODO: Summarize one weekly review using counts and redacted observations rather than raw logs.

## Bitcoin and Lightning Node Lessons

- Record operational lessons about availability, updates, privacy, backups, and separation of duties.
- Never include wallet data, keys, seed or recovery phrases, channel data, addresses, balances, peers, or identifiable network details.
- TODO: Document a fictional or sanitized recovery scenario and the control it tests.

## Mistakes and Improvements

Mistakes should be documented without exaggeration or blame. Focus on the condition, impact, correction, and prevention.

- TODO: Add a sanitized example where documentation, monitoring, or a checklist prevented a repeated mistake.

