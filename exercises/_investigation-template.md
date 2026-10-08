# <CASE_TITLE>

**Status:** PLANNED / IN PROGRESS / COMPLETED — select one based on evidence.

- Exercise ID: `<EXERCISE_ID>`
- Environment: `<SANITISED_LAB_ROLE>`; controlled test / observed event / synthetic dataset (state which).
- Review window and timezone: `<START_UTC>` to `<END_UTC>`.
- Repository revision / rule version: `<COMMIT_OR_VERSION>`.
- Scope, operator role, permitted actions and exclusions: `<SCOPE>`.
- Evidence provenance: `<SOURCE_AND_COLLECTION_METHOD>`; raw material retained privately.

## Detection

What generated the event? Record the trigger, rule/query, event time versus detection time and whether an alert really fired. A manual observation is not a SIEM detection.

## Evidence

List sources actually reviewed, bounded time window, sanitized evidence IDs, collection method, completeness/gaps and relevant event counts. Preserve original timestamps privately. Synthetic/test evidence is labelled; never imply an actual compromise.

## Initial hypothesis

State the hypothesis, confidence, competing benign explanation and what would disprove it.

## Analysis

Separate observations, correlations, assumptions and unknowns. Explain field meaning and negative checks; absence of an alert does not prove absence of activity. Do not substitute an architecture description for investigation.

## Timeline

| UTC or consistent relative time | Evidence ID | Observation / action | Result / uncertainty |
| --- | --- | --- | --- |
| `<TIME>` | `<EVIDENCE_ID>` | `<FACT>` | `<RESULT>` |

## MITRE ATT&CK

Use **Not mapped — insufficient observed behavior** when appropriate. Proposed mappings stay explicitly conditional and out of completed evidence.

| Behavior actually observed | Supporting telemetry / evidence ID | Technique / sub-technique and primary reference | Confidence and limitation |
| --- | --- | --- | --- |
| `<BEHAVIOR_OR_NONE>` | `<TELEMETRY_OR_NONE>` | `<JUSTIFIED_ID_OR_NOT_MAPPED>` | `<HIGH_MEDIUM_LOW_AND_REASON>` |

No technique from a product name, event ID alone, or an unrelated keyword. A simulated behavior can have a technique mapping while its classification remains benign; identify the simulation.

## Query

Record exact query language, engine/version, source/index, fields, time window and the query **actually executed**. Include sanitized result counts and explain query limitations. Proposed SPL, KQL or dashboard filters are labelled unexecuted until run.

## Classification

Choose **True Positive / Benign Positive / False Positive / Inconclusive**, justify with evidence and distinguish a correct alert on approved activity (Benign Positive) from a rule that does not represent the intended condition (False Positive). Operational health reviews may use Inconclusive while pending and N/A — health review on completion; do not invent a security alert.

## Impact

Observed effect, affected sanitized roles, duration and known limits. Separate actual impact from possible impact.

## Containment / Action

State actions actually taken and authority. Record **none** when appropriate. No automatic account lockout, network blocking or endpoint isolation in these first exercises. Preserve private evidence before an approved change.

## Escalation decision

Explain close/monitor/escalate, evidence behind the choice, severity and what new finding would change it. Unexpected success, unexplained execution, persistence or secret exposure requires escalation rather than assumed benignity.

## L2 handoff

For a lab, write a **simulated handoff note**; do not imply a real analyst or ticket queue. Include summary, timeline, evidence IDs, executed queries/results, confidence, scope/impact, actions, gaps, hypothesis and the specific question for L2. No external message is sent.

## Lessons learned

Record what the completed investigation taught, which assumption failed and a concrete next step. Pending exercises have no claimed operational lessons.

## Detection tuning

Record before/after rule versions, rationale, benign control, positive control, retained coverage, result counts and rollback. State **none performed** if no change was tested. Avoid global exclusions for an account/process/domain.

## Sanitisation

Apply [the publication checklist](SANITISATION.md). Use stable placeholders, relative timing when needed, aggregates and original public query syntax. Remove identifiers, raw logs, sensitive command lines and private topology. Record reviewer role and review status without real usernames.

## Completion criteria

- [ ] Activity was performed on an authorized lab or explicitly named dataset.
- [ ] Source, time window, telemetry, executed queries and result counts are recorded.
- [ ] All sections contain evidence or a justified N/A; no placeholders stand in for findings.
- [ ] Classification, impact, escalation/handoff and ATT&CK reasoning are defensible.
- [ ] Proposed actions and tuning are separated from performed actions.
- [ ] Sanitisation and repository validation passed; human diff review completed.
- [ ] Only now mark COMPLETED and add a link to README's Operational evidence.
