# 005 — Detection-rule tuning

**Status: PLANNED — not performed.**

Prerequisites: complete 001 and the applicable gates in the [telemetry roadmap](../../docs/siem-telemetry-roadmap.md). Use the [common investigation template](../_investigation-template.md) for the real report.

## Detection

Planned trigger: A documented noisy or incomplete rule from a completed earlier case, with a measurable tuning question. No event or alert has been generated or reviewed for this case.

## Evidence

Planned sources: Original rule/query version, the approved positive/benign control datasets and actual Wazuh alert/event results before and after. No evidence has been collected.

## Initial hypothesis

Untested: A narrow change can reduce irrelevant alerts while preserving intended behavior coverage.

## Analysis

Planned procedure: Define expected condition, measure before/after on the same bounded dataset/window, keep an independent intended-positive control and explain blind spots. Do not suppress an entire account, executable or domain just to obtain fewer alerts. No findings are asserted.

## Timeline

Not recorded; no investigation performed. Use actual UTC or consistently transformed relative times after execution.

## MITRE ATT&CK

No mapping yet. Inherit only a behavior mapping justified by the source investigation and revalidate coverage after tuning. Rule names or product rule metadata are not sufficient evidence.

Every future mapping must list observed behavior, supporting evidence ID/source, technique/sub-technique and confidence with limitations.

## Query

Record actual original/modified rule or filter, version/hash, exact executed searches, source/window and counts. No rule change or benchmark has been performed.

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

- [ ] A preceding completed case supplies actual noisy/missed behavior.
- [ ] Version original and proposed rule with rationale and rollback.
- [ ] Run equivalent before/after checks with positive and benign controls.
- [ ] Record counts and retained coverage, classify results and document limitations.
- [ ] Finish all common-template sections with evidence or justified N/A.
- [ ] Include incident note, escalation decision and simulated L2 handoff.
- [ ] Pass human sanitisation review and repository validation.
- [ ] Only then mark COMPLETED and link under Operational evidence.
