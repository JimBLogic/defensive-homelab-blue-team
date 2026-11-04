# Defensive Homelab - WSL2 Validation

Date: 2026-11-04
Status: DEGRADED - operational validation, review incomplete
Source commit: b3658b8

## Environment

Ubuntu WSL2 + Docker Desktop
Docker Compose LITE
Four services:
- Uptime Kuma
- Prometheus
- Node Exporter
- Grafana

## Verified Results

- 29/29 automated Python tests passed.
- Four core containers running.
- Prometheus targets: 2/2 UP.
- Grafana datasource connection successful.
- CPU and memory metrics visualized.
- Uptime Kuma monitored Prometheus successfully.
- Two observations separated by 25m 17s.
- Zero restarts and OOM kills in both observations.
- Dashboard ports bound to localhost.
- No privileged core containers.
- no-new-privileges enabled.
- Reviewed read-only mounts and log rotation.

## Automated Baseline

56 PASS
1 FAIL
4 NOT_VERIFIED
18 REVIEW_REQUIRED

## Known Findings

FS-001:
Node Exporter filesystem collector fails when
parsing mount information containing 9P entries.

Four entries with unexpected field structure
were identified among 322 examined entries.

Impact:
Filesystem metrics unavailable through Node Exporter.

Other limitations:
- Grafana mount-source verification discrepancy.
- Uptime Kuma returns HTTP 302 to its dashboard, followed by HTTP 200. The automated collector does not follow redirects.
- Automated Docker storage-capacity checks remain unverified. Independent manual checks were performed; Windows physical disk capacity was not verified.
- Five historical Grafana error-level messages were identified. No further error-level messages appeared during a later 15-minute observation; root causes remain partially unverified.
- Full network exposure and firewall review incomplete.

## Scope

This is evidence of a local WSL2 laboratory.

It does not establish Raspberry Pi deployment,
production readiness, or completion of Exercise 001.

Publication status: DRAFT - NOT APPROVED.
