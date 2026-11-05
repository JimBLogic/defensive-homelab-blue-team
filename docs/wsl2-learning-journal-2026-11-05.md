# Windows 11 + WSL2 Defensive Homelab: Test and Learning Journal

**Session date:** 2026-11-05 (local date; individual test timestamps not republished)  
**Environment:** Windows 11 host, Ubuntu under WSL2, Docker Desktop 4.97.0, Docker Engine 29.9.2 (Linux/amd64), Docker Compose LITE  
**Assessment:** DEGRADED - usable local learning lab with unresolved telemetry, startup and host-boundary checks  
**Evidence source:** Operator-supplied PowerShell/WSL2 results and locally generated private collector reports. Not independently executed by a GitHub reviewer.  
**Target hardware:** Raspberry Pi 4 / ARM64, **NOT TESTED**. Migration deliberately deferred; no SD-card preparation required for this stage.

## Purpose and scope

The original repository targets a Raspberry Pi, but **the environment being operated and tested now is the Windows 11 + WSL2 + Docker Desktop lab**. Treat this as genuine hands-on operational learning with platform-specific limitations, not as a claim of Raspberry Pi deployment. [Initial WSL2 validation](validation-wsl2-2026-11-04.md) records the earlier observation window.

Private report JSON, logs, configuration values, host identities, credentials and full mount paths remain outside the public checkout. This journal only records manually reviewed, minimized observations. Automated CI validates repository code and synthetic fixtures; it cannot verify a live host.

## Stack observed

| Service | Image | Post-recovery observation |
| --- | --- | --- |
| Grafana | `grafana/grafana:13.1.0` | Running, Docker healthcheck healthy; HTTP health, datasource configuration and datasource health PASS |
| Prometheus | `prom/prometheus:v3.13.1` | Initially stopped after a Windows cold boot; subsequently running and healthy after manual `docker start`; `/-/ready` returned HTTP 200 |
| Node Exporter | `prom/node-exporter:v1.12.1` | Running (no configured Docker healthcheck), Prometheus scrape successful; filesystem metric still not verified |
| Uptime Kuma | `louislam/uptime-kuma:2.4.0-slim` | Running, Docker healthcheck healthy; collector HTTP verification NOT_VERIFIED because redirects are not followed |

The shown dashboard host bindings were loopback-only. Complete Windows firewall, LAN reachability, SSH and effective host-boundary reviews remain pending.

## Incident: Prometheus failed to start after Windows shutdown

**Trigger:** Entire Windows 11 PC had been powered off; Ubuntu WSL2 and Docker Desktop were started again.

1. Docker CLI and server were reachable from Ubuntu WSL2.
2. Three services were running, but Prometheus reported `exited (127)`.
3. Docker inspect reported `OOMKilled=False`, `RestartCount=0`, restart policy `unless-stopped`, and a nonempty startup error.
4. Operator-side classification of Docker's error matched OCI/runc execution and Docker Desktop mount paths, including a file-versus-directory mismatch. The error mentioned the Prometheus configuration-file mount, not its targets-directory mount.
5. WSL2 reported the expected configuration as a regular file and its targets location as a directory. Docker reported a matching read-only bind mount for the configuration file. These checks do **not** establish the cause of the failed mount.
6. Manual `docker start` of **the existing Prometheus container** succeeded. Follow-up inspect: `running`, `healthy`, current exit code `0`, restart count `0`; independent readiness request to `/-/ready` returned HTTP `200`.

**Impact:** Temporary Prometheus outage and a potential metrics collection gap following cold boot. Historical time-series continuity and lost-sample duration were **NOT VERIFIED**.

**Root cause:** **Suspected** transient Docker Desktop/WSL2 bind-mount initialization problem; **not confirmed**. The evidence does not justify declaring data corruption or an application bug.

**Recovery performed:** `docker start` only; no Compose recreation, volume deletion, image update or privilege change. Repeat cold-boot behavior and mount initialization require later controlled reproduction.

## Validation of the WSL2 bind-source review candidate

The [merged PR #14](https://github.com/JimBLogic/defensive-homelab-blue-team/pull/14) changes the mount assessment for a Docker Desktop bind-source-path translation from unconditional FAIL to REVIEW_REQUIRED **only** where mount count, destination, type and read-only mode match. The native-Linux and structural-drift checks remain fail-closed.

**CI evidence (PR #14):** GitHub Actions repository validation successful; **31/31 Python synthetic tests passed**, including tests that additional mounts, writable mounts and changed destinations/types still FAIL. This is code-level evidence, not proof of the physical host mount identity.

**Real operator observation:** the private post-recovery collector report contained:

| Check | Outcome | Interpretation |
| --- | --- | --- |
| `grafana.mounts_match` | REVIEW_REQUIRED | Source-path discrepancy remains subject to human confirmation; not an automatic PASS |
| `node-exporter.mounts_match` | PASS | Mount structure matched; does **not** prove the filesystem collector works |
| `prometheus_targets` | PASS | Expected targets up and fresh at observation time |
| `node_exporter_up` | PASS | Node Exporter was being scraped |
| `grafana_http_health` | PASS | Grafana HTTP/database health |
| `grafana_datasource_config` | PASS | Expected Prometheus datasource configuration |
| `grafana_datasource_health` | PASS | Datasource health endpoint responsive |
| `host_cpu_5m_percent` | REVIEW_REQUIRED | Numeric telemetry available; interpretation not completed |
| `host_memory_percent` | REVIEW_REQUIRED | Numeric telemetry available; interpretation not completed |
| `filesystem_available_percent` | NOT_VERIFIED | No usable result; outstanding FS-001/9P investigation |
| `kuma_http` | NOT_VERIFIED | Root redirect intentionally not followed by collector |

**Automated check totals:** **56 PASS / 0 FAIL / 4 NOT_VERIFIED / 19 REVIEW_REQUIRED**. Collector exit code **2**, indicating incomplete review. Compared with the initial WSL2 summary (56 PASS / 1 FAIL / 4 NOT_VERIFIED / 18 REVIEW_REQUIRED), exactly one *mount-path classification* moved from FAIL to REVIEW_REQUIRED. This does **not** mean the filesystem metrics issue is resolved.

## Engineering lessons

- A **running** container, a **healthy** Docker healthcheck, an **UP** Prometheus target and a **working individual metric** are distinct levels of assurance.
- A host can regain service readiness via `docker start` without proving its cold-boot reliability, data persistence or root cause.
- A Docker Desktop-translated bind source requires careful review; automatic normalization to PASS would hide unexpected mount changes.
- Exit code **2** from this repository's baseline collector means incomplete/manual verification, not necessarily an unhandled exception.
- Windows + WSL2 is a valuable real operating environment for defensive monitoring, incident documentation and regression testing; it is **not** equivalent to Raspberry Pi ARM64, native Linux mount behavior or a production exposure review.
- Retain evidence from failed checks rather than disabling filesystem collection, widening permissions or recreating volumes solely to get a green dashboard.

## Next experiments, in priority order

1. **Cold-boot reliability:** capture pre-shutdown state, boot order, Docker mount readiness and Prometheus status across a controlled restart; keep original private error evidence and check metrics continuity.
2. **FS-001:** investigate WSL2 `9p` mountinfo compatibility and the Node Exporter filesystem collector; preserve CPU/memory visibility and test any adjustment independently.
3. **Kuma HTTP:** handle the known redirect only with a constrained, loopback-safe readiness check and synthetic regression tests.
4. **Mount verification:** manually establish that Grafana's translated source points to the intended read-only content; maintain REVIEW_REQUIRED until evidenced.
5. **Host boundary and storage:** validate real disk headroom/retention, Windows firewall and listener exposure, relevant historical logs and effective permissions.
6. **Future Raspberry Pi:** later reproduce configuration and checks on the actual ARM64 host, separately documenting its own results. **No SD-card formatting or migration is scheduled now.**

## Publication and completion limits

**Status: REVIEW DRAFT.** This is a scoped learning and operation report, not a completed incident investigation or evidence that Exercise 001 is finished. The private reports need to be retained by the operator and final human sanitization approved before merging this document into `main`.
