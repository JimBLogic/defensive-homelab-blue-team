# Defensive Homelab - WSL2 LITE Operational Validation

**Observed date:** 2026-11-04 (UTC)  
**Result:** DEGRADED - operating with known telemetry gaps and incomplete manual review  
**Environment:** Ubuntu WSL2 / Docker Desktop; LITE profile  
**Reviewed source revision:** `b3658b8`  
**Publication:** Sanitized WSL2 pilot merged into main via PR #13; Exercise 001 not completed or approved

## Scope and setup

This is a **local WSL2 pilot**, not a Raspberry Pi deployment or a completed Exercise 001. Four core services were started: Uptime Kuma, Prometheus, Node Exporter and Grafana. A temporary WSL2-specific, untracked Compose override was needed for Node Exporter's root mount propagation; the committed Raspberry Pi configuration was not changed. Docker Desktop's filesystem/mount representation is not equivalent to physical Raspberry Pi storage.

## Evidence collection and traceability

Two read-only collector reports were retained **privately outside the repository**. This page contains only selected, manually reviewed findings; raw Docker output, credentials, host paths and logs are not published.

| Evidence ID | Collection time (UTC) | Automated outcome |
| --- | --- | --- |
| WSL2-OBS-01 | 2026-11-04 13:10:41 | 56 PASS / 1 FAIL / 4 NOT_VERIFIED / 18 REVIEW_REQUIRED |
| WSL2-OBS-02 | 2026-11-04 13:35:58 | 56 PASS / 1 FAIL / 4 NOT_VERIFIED / 18 REVIEW_REQUIRED |

**Observation interval:** 25 minutes 17 seconds. No automated status was manually converted to PASS.

Methods: `verify-stack.sh lite`, `baseline-health-review.py`, private Docker state and bounded-log inspection, Grafana datasource/PromQL checks, Prometheus target checks, Uptime Kuma monitor inspection, and local host-listener review. Human checks provide supplementary evidence; they do not change collector outcomes.

## Verified local observations

- All four core containers were running. Three configured healthchecks were healthy; Node Exporter has no Docker healthcheck and was assessed via a successful Prometheus scrape.
- Prometheus reported its two expected targets **UP**, including Node Exporter; CPU and memory metrics were available. The Node Exporter **filesystem** collector was failing separately.
- Grafana datasource connection succeeded, and CPU/memory PromQL queries returned data.
- A configured Uptime Kuma monitor for Prometheus reported **UP** with a 60-second check interval.
- Across both observations: **zero observed container restarts** and **zero OOM kills**.
- Memory usage remained below each container's configured limit in both samples; this is **not** evidence of long-term stability or a load test.
- Local Windows listeners for the three dashboards were bound to `127.0.0.1`; an external LAN/firewall inspection was **not** performed.
- No core service ran as Docker `Privileged`; `no-new-privileges`, selected read-only mounts and JSON log rotation were reviewed. Node Exporter's host PID/rootfs access remains a documented exception.

### Container resource samples

CPU and memory percentages below are point-in-time observations, not capacity forecasts. Memory is expressed as a percentage of the configured container limit.

| Service | CPU: first / second | Memory limit: first / second |
| --- | --- | --- |
| Uptime Kuma | 0.00% / 0.26% | 26.40% / 31.66% |
| Prometheus | 0.13% / 0.15% | 6.41% / 6.22% |
| Node Exporter | 0.00% / 0.00% | 5.67% / 6.55% |
| Grafana | 0.56% / 0.46% | 32.34% / 30.49% |

## Findings and unresolved controls

| ID | Status | Evidence, impact and disposition |
| --- | --- | --- |
| FS-001 | **FAIL - confirmed** | Node Exporter's `filesystem` collector reports a mountinfo parse failure. Of 322 mount entries inspected, four `9p` entries contained an unexpected extra field after the separator; filesystem metrics were unavailable. Exact field content was not inspected. Root cause is strongly associated with WSL2 mount formatting, but the exact malformed field remains unverified. No privileges were expanded and no collector was disabled to hide the failure. |
| GRAF-001 | **FAIL in automated baseline** | The Grafana bind-mount source differed from the WSL pathname expected by the collector under Docker Desktop. Read-only mode and file checksum were checked manually; the automated path assertion remains a failure. |
| KUMA-001 | **NOT_VERIFIED by collector** | The Kuma root returned HTTP 302 to its dashboard; a subsequent request reached HTTP 200. The collector intentionally does not follow redirects. The configured monitor was separately reviewed. |
| STORAGE-001 | **NOT_VERIFIED by collector** | Alternative read-only checks inspected WSL/Docker filesystem views, but these did not establish Windows physical disk headroom, storage growth or retention sufficiency. |
| GRAF-LOG-001 | **REVIEW_REQUIRED** | Five historical Grafana error-level events were identified. None were seen in a later 15-minute window; causes remain partially unclassified, not proven resolved. |
| BOUNDARY-001 | **NOT TESTED fully** | LAN reachability, Windows firewall policy, remote SSH boundary, all effective permissions and physical Raspberry Pi exposure were not comprehensively verified. |

Other automated `REVIEW_REQUIRED` items remain in the private reports and should not be considered closed by this summary.

## Test evidence and limitations

Repository validation (including Compose LITE/FULL rendering) and **29/29 Python unit tests** passed locally. GitHub Actions for this documentation PR is a **separate repository/CI check**; neither static validation nor a green CI job proves live service health.

This pilot demonstrates real local service operation and a reproducible failure investigation. It **does not** establish a production-ready deployment, completed investigation/handoff, Raspberry Pi compatibility or completion of [Exercise 001](../exercises/001-baseline-health-review/README.md).

**Review disposition:** Public draft only. Human publication review and PR approval remain pending; do not label Exercise 001 COMPLETED based on this WSL2 pilot.
