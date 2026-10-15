# Defensive Homelab Blue Team — container security patch audit

**Audit date: 15 October 2026.** **GitHub-only candidate:** `audit/container-security-20261015`, branched from `main` commit `b3658b8bf60ef62f6d2a782b79501d824bb8390e`. Public source repository; private Raspberry Pi 4/SSD environment is **not connected** and has **NOT** been examined. No real container started, updated, stopped or probed.

## Confirmed findings and precise remediations

1. **Prometheus unauthenticated management surface:** Original `deploy/compose.yaml` enabled `--web.enable-lifecycle`, exposing HTTP `/-/reload` and `/-/quit` to callers able to reach the Prometheus HTTP listener. Host loopback forwarding protects against direct LAN access but other containers attached to `monitoring` and local host processes can still reach it. The current health probes need only `/-/ready`; no lab script calls reload or quit. **Removed the flag**, added an exact Prometheus command allowlist and regression tests. Sources: [Prometheus security model](https://prometheus.io/docs/operating/security/), [management API](https://prometheus.io/docs/prometheus/latest/management_api/).
2. **Grafana candidate patch:** 13.1.0 → **13.1.8**, same minor branch. [Official 13.1.8 release](https://github.com/grafana/grafana/releases/tag/v13.1.8) lists CVE-2026-15577, CVE-2026-33374, CVE-2026-93294 and CVE-2026-95502 fixes (among other changes). This alone is not evidence that any given exploit reaches a local Grafana dashboard.
3. **Prometheus LTS patch:** 3.13.1 → **3.13.4**. [Official 3.13.4 release](https://github.com/prometheus/prometheus/releases/tag/v3.13.4) patches HTTP/2 DATA frame fragmentation memory exhaustion (GO-2026-6348) in gRPC and vulnerable UI dependencies.
4. **Uptime Kuma maintenance:** 2.4.0-slim → **2.5.6-slim**, with [official upstream dependency/security maintenance](https://github.com/louislam/uptime-kuma/releases/tag/2.5.6). It crosses the 2.4 → 2.5 minor version boundary, so **never apply without a tested Uptime Kuma SQLite backup/restore and version-upgrade rehearsal**, because an upgraded database may not be backward compatible.
5. **AdGuard Home** (disabled `dns` profile): 0.107.76 → **0.107.79**, [fixes DNS-over-QUIC DoS GHSA-w6v6-f44j-3rj2](https://github.com/AdguardTeam/AdGuardHome/releases/tag/v0.107.79). No LAN DNS configuration changes.
6. **cAdvisor** (disabled `containers` profile): 0.60.5 → **0.60.6** and **Docker Hub `google/cadvisor` → official `ghcr.io/google/cadvisor`**, [upstream crash/stability fixes](https://github.com/google/cadvisor/releases/tag/v0.60.6). **NOT a security fix for `privileged: true` or host socket mounts**; activation requires a separate isolated lab review. Existing documented exception EX-002 remains open.
7. **Node Exporter** 1.12.1 unchanged: reviewed upstream stable release. **CrowdSec** remains on version 1.7.8 but its invalid Docker tag was corrected from `1.7.8-debian` to vendor-published `v1.7.8-debian`; newer 1.8.1 is a distinct optional major/minor migration with version tag/collection compatibility unverified; do not activate a bouncer or claim detection on the dormant profile.
8. **GitHub Actions supply chain:** `actions/checkout` v4.2.2 → v7.0.1 and `actions/upload-artifact` v4.6.2 → v7.0.2, each pinned to the upstream immutable 40-hex SHA, with fixed `ubuntu-24.04` runner, `contents: read`, no saved checkout credentials, no new scheduled jobs.
9. **Composition guardrails** now reject any unreviewed Prometheus HTTP/admin flag or additional command argument. More synthetic tests ensure pinned version candidates and that privileged optional profiles remain opt-in.

## Remaining known risks and non-goals

- **Grafana admin password** is currently supplied via `deploy/.env` into `GF_SECURITY_ADMIN_PASSWORD`; anyone with Docker administrative access may inspect the runtime environment. Future safer port: [Grafana `GF_SECURITY_ADMIN_PASSWORD__FILE` via Docker secrets](https://grafana.com/docs/grafana/latest/setup-grafana/configure-docker/), but changing bootstrap secrets now risks breaking existing credentials. Never commit a real secret or claim Docker secrets are encrypted by default.
- **cAdvisor EX-002** remains deliberately high risk and disabled. `/:/rootfs:ro`, `/var/run:/var/run:ro` and privileged mode provide significant host visibility; `:ro` on a socket is not read-only API access. No automatic privilege reduction without a real compatibility test.
- **Node Exporter EX-001** retains `pid: host` and read-only host root visibility. No new host port. Needs effective user/capability review with private on-device evidence.
- Explicit version tags are mutable registry references; *do not present them as immutable digests*. Verify `linux/arm64` manifest metadata and resolve exact approved manifest digests before an owner-authorized deployment; test all services on real hardware and backup restore first.
- Image registry metadata checks are **not CVE scans** and do not attest actual runtime or host security. Full image CVE inventory, filesystem state, kernel/Docker version, open ports, backups and secrets must be independently verified on the Pi.
- No Uptime Kuma database migration, Prometheus TSDB / Grafana plugin migration or Pi deployment has been exercised. Leave `deploy/.env` untouched, use the new `.env.example` only as an inspected upgrade proposal.

## Deterministic validations / open gates

- `python3 -m unittest discover -s tests -v`: synthetic, read-only code/security tests; must pass.
- `REQUIRE_COMPOSE=1 ./deploy/scripts/validate-repository.sh`: semantic Compose and host-binding guardrails, secret pattern scan, link checks, actual Docker Compose config render of LITE, FULL and explicit profiles. Do not print rendered Compose config because environment values may contain credentials.
- `bash -n` preflight, verifier and validator; no host operations.
- Optional isolated `.github/workflows/arm64-image-audit.yml` checks public **registry manifest metadata only**, not image downloads or actual run; do not claim a pass until GitHub job result is recorded.
- GitHub Actions only, no deployment. **PR DRAFT to main** until explicit approval and private host compatibility checks.

## Pre-deployment owner action (NOT performed)

Privately export consistent snapshots of `uptime_kuma_data`, `prometheus_data`, `grafana_data` (and optional data volumes if those services were already running), test restores to an *isolated* machine, verify new ARM64 image digests and upstream migration notes, and perform staged updates with rollback plan. Never run `docker compose down -v` as part of rollback.

**Status:** security improvements prepared in GitHub, source-level QA to be recorded below; **operational validation still in progress**, Exercise 001 remains IN PROGRESS / NOT VERIFIED. The public resume is not evidence that personal services are deployed.
