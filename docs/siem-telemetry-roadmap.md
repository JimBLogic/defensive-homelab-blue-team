# SIEM / telemetry learning roadmap

**Status: PLANNED. Deployment-ready defensive baseline · operational validation in progress**

## One initial route

**Safe Windows VM + Windows Event Logs / Sysmon → Wazuh on a separate suitable learning host → query → alert → investigation → incident note → tuning.**

Wazuh is the single initial SIEM route. The Pi continues to host the small monitoring baseline. Do not deploy Wazuh manager/indexer/dashboard there, and do not deploy Elastic, Splunk, Sentinel or another SIEM concurrently. Those remain alternative future study options.

Viability is a gate: confirm available host resources, supported architecture/OS, storage, licenses for the Windows VM and isolation before deployment. Wazuh's quickstart recommends 4 vCPU / 8 GiB / 50 GB for its smallest listed 1–25 agent central deployment. Windows VM capacity is **additional**. These figures do not demonstrate that a suitable host is available. If unavailable, continue with Event Viewer / private local telemetry and leave SIEM ingestion pending.

## Gates and inspectable outputs

| Gate | Work | Completion evidence | Current state |
| --- | --- | --- | --- |
| 0 | Operate the existing baseline | Completed 001 with real sanitized findings and manual boundary review. | IN PROGRESS / NOT VERIFIED |
| 1 | Safe Windows VM telemetry | Snapshot/rollback plan, isolated test network, audit policy and actual event fields/times verified. No home/work domain, personal files or exposed RDP. | PLANNED |
| 2 | Single Wazuh learning environment | Private agent ingestion and bounded retention verified; one known generated event found with source ID/time and no silent ingestion gap. | PLANNED |
| 3 | Real query | Correct fields/index/time window, exact executed query, result count and missing-data limitations. | PLANNED |
| 4 | Alert | Narrow rule for an approved benign test, positive/negative controls, actual alert and delay. | PLANNED |
| 5 | Investigation | One of 002–004 completed using observed telemetry and justified classification / ATT&CK. | PLANNED |
| 6 | Incident note | Timeline, impact, actions, escalation decision and **simulated** L2 handoff. | PLANNED |
| 7 | Detection tuning | 005: before/after rule, counts, retained positive coverage, benign control and rollback. | PLANNED |

## Minimal telemetry

Start with Windows Security logon successes/failures (4624/4625, with the required audit policy), System/Application health, and Sysmon process creation (1). Then enable selected network connections (3) and DNS query events (22) only for the approved exercise. Event 3 is disabled by default in Sysmon. Confirm event creation locally before troubleshooting SIEM ingestion.

Use ProcessGuid/parent context and UTC event times for correlation. PowerShell operational logging, including script block data when deliberately enabled, may contain sensitive content; collect only approved test scripts and keep originals private.

Wazuh's Windows agent can read `Security` and `Microsoft-Windows-Sysmon/Operational` using eventchannel sources. Verify the decoded fields against the actual version. **An alert index is not automatically a complete event archive.** Benign process/DNS events may not produce alerts; if the investigation needs them, privately configure and bound the appropriate archive/ingestion path and prove the generated event is searchable. Never infer absence of behavior from an empty alert search.

## Query learning

Primary operational queries use the real Wazuh indexed fields and dashboard's configured Lucene / DQL search mode; label the language correctly. Candidate filters below are **unexecuted**, with a bounded dashboard time range and selected lab-agent filter required before use:

```text
data.win.system.eventID:4625
data.win.system.eventID:4624
data.win.system.eventID:1 AND data.win.system.providerName:"Microsoft-Windows-Sysmon"
data.win.system.eventID:22 AND data.win.system.providerName:"Microsoft-Windows-Sysmon"
```

Confirm index coverage, spelling/types, provider and agent fields from private real records; revise queries rather than assuming an empty result is valid. Record executed filters, window, source fields and aggregate counts in each case.

After the first Wazuh case, learn basic **KQL** using an explicitly synthetic `datatable` in an authorized query-learning environment: `where`, `project`, `summarize`, `count`, `bin`, ordering and joins. Record the executed query and limits separately. This is query-language practice, **not** a Sentinel deployment, and Wazuh DQL is not KQL. A tutorial read or unexecuted query does not count as operation.

## EDR concepts and detection engineering

Learn endpoint sensor versus SIEM, telemetry versus detection, parent/child process correlation, event versus ingestion time, detection coverage, retention, evidence preservation and the consequences of isolation/blocking. Sysmon emits telemetry; it is not an EDR containment product. Wazuh use does not imply experience operating a commercial EDR.

Define a behavior and required telemetry before writing a rule. Test a benign control and intended positive case, explain false/benign positives, preserve telemetry through ingestion, justify mappings, and tune narrowly. No malware download or automatic response is needed for these first cases.

## Primary sources

- [Microsoft Sysmon](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [Windows failed-logon event 4625](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4625)
- [Wazuh quickstart and resource recommendations](https://documentation.wazuh.com/current/quickstart.html)
- [Wazuh Windows event-channel collection](https://documentation.wazuh.com/current/user-manual/capabilities/log-data-collection/configuration.html)
- [KQL overview and tutorials](https://learn.microsoft.com/en-us/kusto/query/)
