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

The new `deploy/compose.wsl2.yaml` is **opt-in** and overrides only `node-exporter.command`. It keeps `--path.rootfs=/host` and the original exclusions (`/dev`, `/proc`, `/sys`, Docker and containers storage paths), while excluding mount-points ending in or below **any path segment** `/wsl/docker-desktop-bind-mounts`.

It **does not** exclude all `tmpfs`, the WSL2 root filesystem, physical disks, `/mnt/storage` or broad `/mnt/host` paths. The baseline `compose.yaml` is unchanged; no privilege or port adjustments are made.

Synthetic regression tests check both expected exclusions and preserved paths. These tests are not equivalent to a runtime check.

## Safe dry-run (prior to changes)

The existing WSL2 pilot already uses a local **untracked override** to adapt Node Exporter root bind propagation. Do not overwrite that file or run a generic `docker compose up`. Before any runtime changes, identify the existing Compose file stack and compare the **rendered Node Exporter** configuration privately. Compose files must be specified in the actual order, for example:

```text
compose.yaml -> compose.lite.yaml -> existing-local-override -> compose.wsl2.yaml
```

The final override replaces **only** the Node Exporter `command`. Verify original `read_only`, `pid`, `volumes`, `networks`, `security_opt`, `mem_limit`, `pids_limit`, `cpus` and absence of published exporter ports remain intact. Render with `docker compose config --quiet` and avoid uploading rendered configurations with credentials.

Before approving recreation, check exact active project name, files, env values, mount choices and existing named volumes. Do not recreate Grafana/Prometheus/Kuma or use `down -v`. Runtime testing, if later authorized, should replace **only** the Node Exporter container with `up -d --no-deps --force-recreate node-exporter` using the reviewed complete Compose file stack, after recording rollback state.

## Live acceptance / rollback criteria

1. Prometheus continues to scrape Node Exporter, as well as itself, and Grafana datasource health remains PASS.
2. In a defined recent window, filesystem duplicate-series errors drop to zero **after recreation**.
3. `node_filesystem_size_bytes` and `node_filesystem_avail_bytes` return **non-zero series counts** for relevant, non-internal mountpoints, and the baseline collector's `filesystem_available_percent` changes from NOT_VERIFIED to a reviewable value.
4. Privileges, root mount, networks and exporter port exposure do not expand. Verify actual host filesystems are visible, not merely that the exporter reports `success=1`.
5. If series are still absent, errors recur, or non-Docker-Desktop mounts disappear, mark **FAIL**, restore the original Compose file stack and recreate **only** Node Exporter after explicit approval.

Private log details, filenames, secrets and complete mount paths stay outside GitHub. The WSL2 finding **FS-001 remains open** until operator-reviewed runtime evidence satisfies these criteria.
