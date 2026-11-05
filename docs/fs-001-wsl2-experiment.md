# FS-001 — WSL2 Node Exporter filesystem telemetry recovery

**Observed:** 2026-11-05 · Windows 11 / Ubuntu WSL2 / Docker Desktop · LITE
**Status:** **OPERATIONAL RECOVERY VERIFIED IN WSL2** by operator runtime checks; source PR remains **Draft** pending independent CI/review and monitoring.
**Raspberry Pi 4 / native Linux:** **NOT TESTED**; shared `deploy/compose.yaml` remains unchanged.
**Exercise 001:** **IN PROGRESS**, not completed by this fix.

## Symptom and root-cause assessment

Before the correction, Prometheus reported Node Exporter `UP=1` and the filesystem collector success signal `=1`, yet `count(node_filesystem_size_bytes{job="node-exporter"})` and `count(node_filesystem_avail_bytes{job="node-exporter"})` both yielded **zero usable series**. Recent Node Exporter logs contained duplicate-series errors mentioning `node_filesystem_device_error` and `node_filesystem_readonly` with `tmpfs` labels. A bounded excerpt showed **three distinct** problematic mountpoint labels in Docker Desktop's `/wsl/docker-desktop-bind-mounts/` subtree; 54 is the number of label *occurrences*, not a count of distinct mounts. A separate earlier WSL2 observation found four unusual `9p` mount-info entries; whether these were the same root cause remains **UNVERIFIED**.

The working diagnosis is **Docker Desktop-specific internal bind mounts triggering filesystem metric collisions**, not a native Raspberry Pi filesystem problem. The exclusion addressed the observed symptom; no claim is made to have fixed Docker Desktop itself.

## Opt-in fix and rollback

- `deploy/compose.wsl2.yaml`: overrides **only Node Exporter** `volumes` and `command`, setting the previously observed effective root bind `/:/host:ro` and keeping `--path.rootfs=/host`. The filesystem exclusion retains baseline system/container storage exclusions, adding the Docker Desktop `/wsl/docker-desktop-bind-mounts` subtree. **It does not exclude all tmpfs, /, /mnt/storage or broad /mnt/host paths.**
- `deploy/compose.wsl2.rollback.yaml`: restores the **original Node Exporter command** plus the observed WSL2-only `/:/host:ro` mount. Docker Compose uses `$$` to represent the literal `$` regex anchor passed to the container. An observed 113-versus-114-character discrepancy was verified to be *only* this escaping difference.
- Neither overlay alters the native-Linux/Raspberry Pi base `/:/host:ro,rslave` mount or adds ports, capabilities, privileged mode, credentials or networks.
- The previous operator-specific, untracked Compose override lived in a temporary directory and is **no longer present**. It must **not** be used in new invocations. The durable opt-in overlay reconstructs its observed mount semantics.

The approved WSL2 operator file stack was:

```text
compose.yaml -> compose.lite.yaml -> compose.wsl2.yaml
```

The rollback file, when explicitly needed, must **replace** `compose.wsl2.yaml` as the final overlay. Never include both overlays in one invocation. Keep the same existing project name `defensive-homelab-wsl-test` and private `.env`; never publish the rendered full configuration, complete Docker inspect or raw logs. Do not use `docker compose down -v` or modify optional profiles.

## Preflight evidence

Operator-provided local observations on the WSL2 experiment branch:

| Check | Result |
| --- | --- |
| Python unit suite after rollback tests were added | **33/33 OK, exit 0** |
| Candidate `docker compose config --quiet` | **PASS**, exit 0 |
| Rollback `docker compose config --quiet` | **PASS**, exit 0 |
| Candidate sanitized security/config projection | **12/12 true** |
| Rollback-vs-running-container sanitized critical settings | **12/12 true** |
| Proposed mount filter vs 3 observed problem mount labels | **3/3 excluded** |
| Sampled root/storage/system/container paths | No new exclusion except Docker Desktop subtree |

These tests alone are **not** runtime evidence or an executed rollback.

## Approved runtime intervention and acceptance

After explicit operator approval, the operator ran **only**:

```bash
COMPOSE_PROJECT_NAME=defensive-homelab-wsl-test docker compose \
  --env-file .env -f compose.yaml -f compose.lite.yaml -f compose.wsl2.yaml \
  up -d --no-deps --force-recreate node-exporter
```

The actual operator invoked equivalent absolute paths from Windows PowerShell. Docker reported **1/1 container started**, exit **0**. Post-change inspection confirmed a **new container ID**, running state, read-only root filesystem and non-privileged execution. No other Compose service was requested for recreation.

The operator's post-change read-only checks then reported:

| Live check | Observed result | Interpretation |
| --- | --- | --- |
| `up{job="node-exporter"}` | **1** | Scrape target operational |
| `node_scrape_collector_success{job="node-exporter",collector="filesystem"}` | **1** | Collector reports success |
| `count(node_filesystem_size_bytes{job="node-exporter"})` | **9** (previously **0**) | Capacity series recovered |
| `count(node_filesystem_avail_bytes{job="node-exporter"})` | **9** (previously **0**) | Available-space series recovered |
| Count with size greater than zero | **9** | Nonzero capacity |
| Count with available bytes at least zero | **9** | Nonnegative available-space values |
| Non-temporary filesystem size series greater than zero, excluding `tmpfs|ramfs|overlay|9p|autofs|squashfs` | **4** | Useful non-temporary metrics observed, not proof of physical Windows disk headroom |
| `up{job="prometheus"}` | **1** | Self-monitoring operational |
| Docker health of Grafana / Prometheus / Uptime Kuma | **HEALTHY / HEALTHY / HEALTHY** | Three unaffected services healthy at inspection time |
| Bounded Docker logs since new Node Exporter start | **58 lines**, read OK, fewer than 500 | Post-recreation log inspection |
| Duplicate-series error patterns | **0 matches** | No matching duplicate errors in sampled logs |
| Mountinfo/parse error patterns | **0 matches** | No matching parse errors in sampled logs |

**Disposition:** **FS-001 operational recovery verified for the WSL2 pilot at the measured points in time.** The original zero-series symptom is demonstrably removed. This does **not** establish long-term stability, Raspberry Pi equivalence, full log coverage, or completion of the broader Homelab Exercise 001.

## Remaining controls and follow-up

1. **Independent collector evidence:** `baseline-health-review.py` currently builds the base/LITE Compose file stack without the WSL2 overlay. Do not interpret its default mount comparison as an accurate assessment of the WSL2-specific pilot. Reconcile collector support for opt-in WSL2 overlays separately before treating its `filesystem_available_percent` field as closed.
2. **Sustained operation:** repeat metrics/duplicate checks after normal restarts and a later cold boot. Future failures should reopen FS-001; the old Docker Desktop mount translation and historical `9p` anomaly are not guaranteed fixed.
3. **Rollback:** statically validated and matched to the original runtime's essential fields, but **NOT TESTED LIVE**. Apply only if required and authorized, using the same private env/project, single-service recreation and immediate post-change checks.
4. **CI and publication:** the PR remains **Draft** while independent GitHub Actions runs cannot start runner steps (tracked in issue #17); local 33/33 tests do not replace required CI policy or an approved exception.
5. **Storage boundary:** nine exporter mount series and four non-temporary series do not establish physical Windows volume free space, SSD condition or future Raspberry Pi filesystem compatibility. Validate those separately.

**Privacy:** only sanitized counts, mount-category patterns and operator-approved observations are recorded in this public source file. No host-specific raw log paths, credential values or private labels are published.
