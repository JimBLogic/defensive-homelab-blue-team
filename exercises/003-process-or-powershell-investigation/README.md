# 003 — Process / PowerShell investigation

**Status: PLANNED — not performed.**

Prerequisites: complete 001 and the applicable gates in the [telemetry roadmap](../../docs/siem-telemetry-roadmap.md). Use the [common investigation template](../_investigation-template.md) for the real report.

## Detection

Planned trigger: A harmless approved PowerShell process test in the isolated Windows VM, observed manually or through a genuinely tested rule. No event or alert has been generated or reviewed for this case.

## Evidence

Planned sources: Sysmon process creation with parent/child ProcessGuid and command context; PowerShell operational logging if safely enabled; selected Wazuh ingestion. No evidence has been collected.

## Initial hypothesis

Untested: The process is approved lab activity; unexpected parentage, script content or downstream activity requires further review.

## Analysis

Planned procedure: Reconstruct parent/child chain, time, account role and command purpose. Use a harmless local command such as Get-Date; no downloads, persistence, encoded payload or bypass is required. Review what is visible and absent. No findings are asserted.

## Timeline

Not recorded; no investigation performed. Use actual UTC or consistently transformed relative times after execution.

## MITRE ATT&CK

No observed mapping yet. When PowerShell execution is actually evidenced, assess [T1059.001 — PowerShell](https://attack.mitre.org/techniques/T1059/001/) with ProcessGuid/command telemetry, confidence and the explicitly benign test context. Tool presence alone is insufficient.

Every future mapping must list observed behavior, supporting evidence ID/source, technique/sub-technique and confidence with limitations.

## Query

Use actual Sysmon/provider/process fields and the selected bounded Wazuh index. Record exact executed filters and counts; do not invent a process tree or claim untested rule detection.

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

- [ ] Capture and correlate actual process and parent telemetry.
- [ ] Explain command purpose and any logging gaps.
- [ ] Distinguish observed behavior, tested alert and malicious intent.
- [ ] Publish a sanitized process-chain summary and justified classification.
- [ ] Finish all common-template sections with evidence or justified N/A.
- [ ] Include incident note, escalation decision and simulated L2 handoff.
- [ ] Pass human sanitisation review and repository validation.
- [ ] Only then mark COMPLETED and link under Operational evidence.
