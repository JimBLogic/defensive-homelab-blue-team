# 004 — Network / DNS investigation

**Status: PLANNED — not performed.**

Prerequisites: complete 001 and the applicable gates in the [telemetry roadmap](../../docs/siem-telemetry-roadmap.md). Use the [common investigation template](../_investigation-template.md) for the real report.

## Detection

Planned trigger: One controlled DNS query or local test connection from a known process on the isolated test VM. No event or alert has been generated or reviewed for this case.

## Evidence

Planned sources: Selected Sysmon 22 DNS events and, if deliberately enabled, Sysmon 3 network events; approved test resolver/service and Wazuh ingestion. No evidence has been collected.

## Initial hypothesis

Untested: The queried destination and process belong to the approved test; unknown activity remains unexplained until correlated.

## Analysis

Planned procedure: Compare ProcessGuid, query/connection time, direction, response and approved test intent. Use a controlled lab resolver/service; no personal browsing collection, internet scan or raw DNS-history export. No findings are asserted.

## Timeline

Not recorded; no investigation performed. Use actual UTC or consistently transformed relative times after execution.

## MITRE ATT&CK

Not mapped. DNS resolution or a network connection alone is not evidence of C2, discovery or exfiltration. Assign a technique only if additional observed behavior supports it; explain the telemetry and confidence.

Every future mapping must list observed behavior, supporting evidence ID/source, technique/sub-technique and confidence with limitations.

## Query

Check real provider/eventID/process fields and archive coverage. Record exact executed agent/time/process filters and aggregate counts. Sysmon network events are not enabled by default.

## Classification

Not assessed — PLANNED. After execution select True Positive / Benign Positive / False Positive / Inconclusive with evidence. A harmless authorized test can be a Benign Positive; an unexecuted plan is not a classified event.

## Impact

Not assessed. Any approved test should have minimal, bounded lab impact; observed impact must be recorded after execution.

## Containment / Action

None performed. No automatic blocking, lockout or isolation is planned. Preserve private evidence and request an operator decision if unexpected activity warrants a host change.

## Escalation decision

Not made. Unexplained success/execution, secret exposure or broader activity would require an evidence-based escalation decision.

## L2 handoff

Not written. Produce a simulated handoff from actual findings: summary, timeline, evidence IDs, queries/results, actions, impact, confidence, gaps and a specific question for L2. No real L2 contact or escalation is claimed.

## Lessons learned

None from live execution. Record actual lessons after completing the case.

## Detection tuning

None performed. Record measured changes only when tested; preserve positive-control coverage and rollback.

## Sanitisation

No live evidence published. Follow [the checklist](../SANITISATION.md); keep raw events, names, addresses, command lines with sensitive values, DNS history and screenshots private.

## Completion criteria

- [ ] Prove event capture and searchable ingestion for the controlled activity.
- [ ] Correlate process with the actual DNS/connection evidence and state gaps.
- [ ] Classify the activity without equating DNS use to C2.
- [ ] Publish only bounded counts, roles and a sanitized timeline, never browsing history.
- [ ] Finish all common-template sections with evidence or justified N/A.
- [ ] Include incident note, escalation decision and simulated L2 handoff.
- [ ] Pass human sanitisation review and repository validation.
- [ ] Only then mark COMPLETED and link under Operational evidence.
