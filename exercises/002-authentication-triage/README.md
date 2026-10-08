# 002 — Authentication triage

**Status: PLANNED — not performed.**

Prerequisites: complete 001 and the applicable gates in the [telemetry roadmap](../../docs/siem-telemetry-roadmap.md). Use the [common investigation template](../_investigation-template.md) for the real report.

## Detection

Planned trigger: Approved failed-logon test followed by an authorized success, or a bounded manual authentication review. No event or alert has been generated or reviewed for this case.

## Evidence

Planned sources: Windows Security 4625/4624 with audit policy and the selected Wazuh event/alert sources verified. No evidence has been collected.

## Initial hypothesis

Untested: A small approved test explains the failures; an unexpected success or source would change the assessment.

## Analysis

Planned procedure: Correlate time, sanitized account/host role, logon type, failure reason and subsequent success. Check lockout policy first; use a spare lab account and few attempts, never brute force a live account. No findings are asserted.

## Timeline

Not recorded; no investigation performed. Use actual UTC or consistently transformed relative times after execution.

## MITRE ATT&CK

No mapping yet. Repeated failures alone do not prove password guessing. Only if observed behavior and telemetry support it, assess [T1110.001 — Password Guessing](https://attack.mitre.org/techniques/T1110/001/), identify approved simulation versus suspicious activity and state confidence.

Every future mapping must list observed behavior, supporting evidence ID/source, technique/sub-technique and confidence with limitations.

## Query

Start from the real decoded eventID fields; record the bounded agent/time filters, exact executed dashboard query and result counts. No query has been run.

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

- [ ] Prove log creation and ingestion coverage for both failures and successes.
- [ ] Correlate the bounded test with logon type/reason and authorized activity.
- [ ] Justify classification; document whether escalation is needed.
- [ ] Record ATT&CK only when behavior supports it; no brute-force claim from a failed event.
- [ ] Finish all common-template sections with evidence or justified N/A.
- [ ] Include incident note, escalation decision and simulated L2 handoff.
- [ ] Pass human sanitisation review and repository validation.
- [ ] Only then mark COMPLETED and link under Operational evidence.
