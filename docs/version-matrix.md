# Version Matrix — security patch candidates

**Reviewed 2026-10-15; CrowdSec baseline/candidate correction verified 2026-10-16.** Exact *version tags*, **not immutable content digests**, are declared in `deploy/.env.example`. These are **candidates only** and have **not** been deployed to or health-checked on the Raspberry Pi 4. Real `deploy/.env` and named-volume content are outside this public repository.

| Component | Previous pin | New candidate tag | Verified upstream purpose | Migration decision |
| --- | --- | --- | --- | --- |
| Uptime Kuma | `louislam/uptime-kuma:2.4.0-slim` | `louislam/uptime-kuma:2.5.6-slim` | Security dependency updates in [2.5.6](https://github.com/louislam/uptime-kuma/releases/tag/2.5.6). | 2.4 → 2.5 version change: **backup and isolated restore test mandatory** before host update. |
| Prometheus | `prom/prometheus:v3.13.1` | `prom/prometheus:v3.13.4` | 3.13 LTS security maintenance: [HTTP/2/gRPC DoS, UI dependency fixes](https://github.com/prometheus/prometheus/releases/tag/v3.13.4). | Same LTS line; verify retention and TSDB rollback. |
| Node Exporter | `prom/node-exporter:v1.12.1` | *unchanged* | Most recent reviewed stable release on [official project](https://github.com/prometheus/node_exporter/releases/tag/v1.12.1). | Do not churn. |
| Grafana | `grafana/grafana:13.1.0` | `grafana/grafana:13.1.8` | [13.1 security maintenance](https://github.com/grafana/grafana/releases/tag/v13.1.8) fixes CVE-2026-15577, CVE-2026-33374, CVE-2026-93294, CVE-2026-95502 and other bugs. | Same 13.1 line; backup DB, check plugins/provisioning. |
| cAdvisor (disabled) | `google/cadvisor:v0.60.5` | `ghcr.io/google/cadvisor:0.60.6` | [Minor stability fixes](https://github.com/google/cadvisor/releases/tag/v0.60.6), not an authorization to enable privileged mode. | Keep `containers` profile OFF. |
| AdGuard Home (disabled) | `adguard/adguardhome:v0.107.76` | `adguard/adguardhome:v0.107.79` | [Security fixes](https://github.com/AdguardTeam/AdGuardHome/releases/tag/v0.107.79), including DNS-over-QUIC exhaustion (GHSA-w6v6-f44j-3rj2). | Keep `dns` profile OFF; do not change LAN DNS. |
| CrowdSec (disabled) | `crowdsecurity/crowdsec:1.7.8-debian` (**invalid old tag**) | `crowdsecurity/crowdsec:v1.7.8-debian` (**verified**) | [Upstream 1.8.1](https://github.com/crowdsecurity/crowdsec/releases/tag/v1.8.1) exists, but it is a separate 1.7 → 1.8 migration with acquisition and image-variant compatibility unverified. | Keep `detection` profile OFF; [seven-image ARM64 registry-manifest CI](https://github.com/JimBLogic/defensive-homelab-blue-team/actions/runs/38737509264) passed with the corrected `v`-prefixed Docker Hub tag. Upstream [CrowdSec GitHub package](https://github.com/crowdsecurity/crowdsec/pkgs/container/crowdsec/856330958?tag=v1.7.8-debian) also lists that version's ARM64 variant on GHCR. These facts do **not** validate a running container or justify upgrading to 1.8. |

## Security decisions beyond image versions

1. `--web.enable-lifecycle` was **removed** from Prometheus. This disables unauthenticated HTTP `/-/reload` **and** `/-/quit` handlers; it is unnecessary for current probes. See [Prometheus' security model](https://prometheus.io/docs/operating/security/) and [management API](https://prometheus.io/docs/prometheus/latest/management_api/).
2. No broad `latest` tags or prereleases; no automatic pulling or deploy. GitHub CI verifies syntax, profiles and restrictions, not that updated images run correctly on the Pi.
3. Tags can be retargeted by registries. Before real deployment, resolve each reviewed tag to a **multi-platform manifest digest**, confirm `linux/arm64` support, record immutable `@sha256` references for the correct artifact, and repeat configuration/tests with those digests. Never substitute an `amd64` digest for the ARM64 image.
4. Do not run `docker compose up`, `pull`, `down -v` or copy .env defaults on the production Pi as part of this GitHub-only change. Back up and restore-test `uptime_kuma_data`, `grafana_data`, and `prometheus_data` with an isolated destination and record compatibility with new app versions. AdGuard and CrowdSec remain off unless separately authorized.
5. **High-risk cAdvisor** still has `privileged:true` and broad host mounts under an opt-in profile. Its version bump fixes bugs but **does not fix this privilege risk**. Do not run cAdvisor for the baseline without separate, tested privilege reduction and owner approval.
6. Grafana still receives an admin password through a private local `.env` value; operators with Docker API access can inspect environment variables. Replacing this with Grafana's supported `GF_SECURITY_ADMIN_PASSWORD__FILE` / Docker secrets is recommended for an independently tested release. See [official Docker secret documentation](https://grafana.com/docs/grafana/latest/setup-grafana/configure-docker/). **Do not place real secret files in Git.**
7. This public repository contains **only infrastructure configuration and synthetic checks**, not evidence of a running homelab. Never present GitHub runner checks as live RPi operation.

## Safe pre-deployment checklist (read-only on the actual host)

```bash
cd deploy
./scripts/validate-repository.sh
./scripts/preflight-check.sh lite
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config --quiet
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml ps
```

The above checks reference the actual local `.env`; do not overwrite it with the newer example. Validate manifests and release notes **before** any pull, then rehearse recovery on a **separate** Docker host. The check is incomplete if Docker/Compose are unavailable.
