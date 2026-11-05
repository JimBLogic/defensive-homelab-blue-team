# FS-001 — Opt-in WSL2 filesystem collector experiment

**Status:** CANDIDATE / NOT TESTED AGAINST LIVE CONTAINERS  
**Target:** Windows 11 + Ubuntu WSL2 + Docker Desktop, LITE lab only.  
**Original target:** Raspberry Pi 4 / native Linux remains **NOT TESTED** and unchanged.

## Evidence and hypothesis

A read-only investigation of the running local Node Exporter found:
- Prometheus target **UP**, `node_scrape_collector_success{collector="filesystem"} = 1`, but **zero** `node_filesystem_size_bytes` and `node_filesystem_avail_bytes` series.
- Nine recent filesystem log errors contained a duplicate-series message; `node_filesystem_device_error` and `node_filesystem_readonly` occurred in these messages.
- The log excerpt contained **54** instances of the `fstype=tmpfs` label, corresponding to **3 distinct** mount-point labels. All three labels contained `/wsl/docker-desktop-bind-mounts/`, across the `/run/desktop/`, `/mnt/host/` and other Docker Desktop variants.
- These counts are log text occurrences, not necessarily distinct mount records. Historical `9p` mount-info parse failures remain separate evidence; the exact root cause is **NOT VERIFIED**.

**Hypothesis:** The internal Docker Desktop bind-mount subtree triggers filesystem metric duplicates in Node Exporter under WSL2. The proposed narrow mount-point exclusion may restore the other filesystem metrics. **It does not prove the underlying Docker Desktop bug is fixed.**

## Proposed change

The new `deploy/compose.wsl2.yaml` is **opt-in** and overrides two fields **only for Node Exporter**: `volumes` and `command`. Docker inspect of the existing WSL2 container reported precisely one `/:/host:ro` bind mount (no explicit propagation), with effective runtime propagation `rprivate`. The original temporary override file is missing even though its parent directory still exists. This checked mount specification is now represented persistently as `volumes: ["/:/host:ro"]`, replacing the native Linux base `/:/host:ro,rslave` **only when this WSL2 overlay is selected**. The `command` retains `--path.rootfs=/host` and the original exclusions (`/dev`, `/proc`, `/sys`, Docker and containers storage paths), while excluding the Docker Desktop `/wsl/docker-desktop-bind-mounts` subtree.

It **does not** exclude all `tmpfs`, the WSL2 root filesystem, physical disks, `/mnt/storage` or broad `/mnt/host` paths. The baseline `compose.yaml` is unchanged; no privilege or port adjustments are made.

Synthetic regression tests check both expected exclusions and preserved paths. These tests are not equivalent to a runtime check.

## Safe dry-run (prior to changes)

The existing WSL2 pilot **was** created using an untracked temporary mount-propagation override, but that file no longer exists in the recorded temporary location. The new opt-in WSL2 overlay intentionally consolidates the *observed* `/host` mount and filesystem filter in a **single durable file**. Do not try to use the missing temporary file or run a generic `docker compose up`.

First record a clean Git worktree and update the WSL2 experiment branch. For a **read-only dry-run**, the intended file order is now:

```text
compose.yaml -> compose.lite.yaml -> compose.wsl2.yaml
```

Use the same private `.env` and project name as the active pilot; do **not** print the full rendered Compose configuration because it may contain credentials. Validate with `docker compose config --quiet`, then inspect **only a sanitized** Node Exporter projection: service set, image tag category, `command`, `volumes`, read-only, PID mode, networks, security options, resource limits and lack of published exporter ports. The effective mount `/:/host:ro` is WSL2-specific; **the Raspberry Pi base remains `/:/host:ro,rslave`**. Docker Desktop's `rprivate` runtime report is not by itself proof of the correct propagation semantics.

Before approving recreation, check exact active project name, files, env values, mount choices and existing named volumes. Do not recreate Grafana/Prometheus/Kuma or use `down -v`. Runtime testing, if later authorized, should replace **only** the Node Exporter container with `up -d --no-deps --force-recreate node-exporter` using the reviewed complete Compose file stack, after recording rollback state.

## Live acceptance / rollback criteria

1. Prometheus continues to scrape Node Exporter, as well as itself, and Grafana datasource health remains PASS.
2. In a defined recent window, filesystem duplicate-series errors drop to zero **after recreation**.
3. `node_filesystem_size_bytes` and `node_filesystem_avail_bytes` return **non-zero series counts** for relevant, non-internal mountpoints, and the baseline collector's `filesystem_available_percent` changes from NOT_VERIFIED to a reviewable value.
4. Privileges, root mount, networks and exporter port exposure do not expand. Verify actual host filesystems are visible, not merely that the exporter reports `success=1`.
5. If series are still absent, errors recur, or non-Docker-Desktop mounts disappear, mark **FAIL**, restore the original Compose file stack and recreate **only** Node Exporter after explicit approval.

Private log details, filenames, secrets and complete mount paths stay outside GitHub. The WSL2 finding **FS-001 remains open** until operator-reviewed runtime evidence satisfies these criteria.
