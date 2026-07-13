# Roadmap

This roadmap tracks a realistic progression from safe documentation to small defensive exercises. Checked items exist as documentation; deployments and operational exercises remain unchecked until they are performed and recorded safely.

## Phase 1: Documentation and Privacy Baseline

- [x] Define repository sanitization and placeholder rules.
- [x] Document architecture, trust boundaries, and exposure categories.
- [x] Define the Blue Team scope and remove unrelated service directions.
- [x] Document Raspberry Pi tool-selection criteria and staged priorities.
- [ ] Re-run the privacy and link review before every public release.

## Phase 2: Lightweight Monitoring Baseline

- [x] Document Uptime Kuma service-check use cases.
- [x] Document Prometheus metrics and retention planning.
- [x] Document Node Exporter host-health planning.
- [x] Document Grafana dashboard and sanitization planning.
- [x] Prepare a local-only default Docker baseline under `deploy/`.
- [ ] Deploy and validate Uptime Kuma as the first operational tool.
- [ ] Complete Operational Exercise 001 and record sanitized results.
- [ ] Define a small approved set of service checks and incident thresholds.
- [ ] Add Prometheus, Node Exporter, and Grafana only after the first tool is stable.

## Phase 3: Container and Host Visibility

- [x] Document Docker monitoring risks and selection questions.
- [x] Add container restart and host resource checks to the review routine.
- [x] Maintain a privacy-aware log review checklist.
- [ ] Select a least-privilege container metrics approach.
- [ ] Record a sanitized host resource baseline.
- [ ] Investigate one container restart or health-check event.

## Phase 4: DNS and Network Defense

- [x] Select AdGuard Home as the documented DNS security candidate.
- [x] Document local-only administration and privacy requirements.
- [ ] Define a blocked-domain review workflow using sanitized summaries.
- [ ] Record false-positive handling without publishing browsing history.
- [ ] Complete a network exposure review for dashboards and metrics endpoints.

## Phase 5: Detection and Response

- [x] Document CrowdSec as a staged log-based detection candidate.
- [x] Maintain a reusable incident response note template.
- [x] Define the Weekly Homelab Log Review exercise.
- [ ] Complete and record the first weekly review.
- [ ] Open a sanitized incident note if an abnormal event is identified.
- [ ] Evaluate alert thresholds and false-positive handling after a normal baseline exists.

## Phase 6: Future Advanced Lab

- [x] Document why advanced tools require separate evaluation.
- [ ] Evaluate Loki with Promtail or Alloy after basic log review is established.
- [ ] Evaluate Suricata only with suitable network visibility and performance capacity.
- [ ] Test Zeek in an external lab better suited to packet analysis.
- [ ] Explore Wazuh through an external x86 deployment or limited agent-only path.
- [ ] Keep Security Onion in an external x86 lab, not on the Raspberry Pi.
