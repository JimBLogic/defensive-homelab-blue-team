# Commands and queries — Exercise 001

**Prepared, not executed against the homelab.** Run locally on the authorized host, keep raw results private, and use the same Compose mode as deployment. Default: LITE with no optional profiles.

## Automated read-only collection

From the repository root:

```bash
./deploy/scripts/validate-repository.sh
cd deploy
./scripts/preflight-check.sh lite
./scripts/verify-stack.sh lite
python3 scripts/baseline-health-review.py --mode lite --output /tmp/baseline-health-review-a.json
# After at least five minutes of normal operation, run a second observation:
python3 scripts/baseline-health-review.py --mode lite --output /tmp/baseline-health-review-b.json
```

Use `full` consistently for a FULL deployment. FULL alone still reviews the four core services. Collector `--profile containers`, `--profile dns` or `--profile detection` is only for a separately approved optional-service review; it does not enable a service. cAdvisor is not needed for 001.

The collector uses Python 3.9+ standard-library modules and Docker Compose v2. It requires a **local Unix-socket** daemon; it refuses a remote/TCP context so local filesystem checks are not attributed to a remote host. A missing CLI, daemon, environment, API response or empty metric stays NOT VERIFIED. It does not install dependencies, start services, modify configuration or send evidence elsewhere.

Exit codes: `0` all recorded checks passed; `1` at least one failed; `2` unavailable/manual observations remain. Manual checks always remain pending until a person reviews them, so an otherwise healthy collection normally exits `2`. Output files are mode 0600, exclusive-create (no overwrite), and must be outside the checkout. Never add collector JSON to Git.

## Private Docker/host inspection

These commands can display sensitive runtime metadata. Do not paste their raw output into the repository:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config --quiet
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml ps --all
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml logs --since 30m --tail 200
docker stats --no-stream
ss -lntu
free -m
df -h
```

Review only project containers for the evidence summary. Inspect actual PortBindings, health status (without healthcheck log output), cumulative RestartCount, OOMKilled, SecurityOpt, Privileged, PidMode, mounts, logging options and resource limits. Identify the Docker data and Prometheus-volume filesystem privately; `df` on the checkout alone is insufficient. Review ports across IPv4 and IPv6 and distinguish configured ports from actual host reachability.

## Prometheus targets and queries

Privately inspect `/api/v1/targets` and the Targets UI. Required jobs are `prometheus` and `node-exporter`, exactly one of each in this baseline. Check up/down, last scrape age, missing/extra targets and scrape errors. Raw endpoint responses contain host labels and are not published.

Execute in Prometheus; record language **PromQL**, actual time window and aggregate results:

```promql
up{job="prometheus"}
up{job="node-exporter"}
100 * (1 - avg(rate(node_cpu_seconds_total{job="node-exporter",mode="idle"}[5m])))
100 * (1 - node_memory_MemAvailable_bytes{job="node-exporter"} / node_memory_MemTotal_bytes{job="node-exporter"})
100 * node_filesystem_avail_bytes{job="node-exporter",fstype!~"tmpfs|overlay|squashfs"}
  / node_filesystem_size_bytes{job="node-exporter",fstype!~"tmpfs|overlay|squashfs"}
```

A cold start may have no five-minute CPU rate yet. Treat this as missing baseline, not zero CPU. Filesystem labels remain private; a minimum percentage is a conservative hint across selected filesystems, not proof of Docker/SSD headroom. Record storage-specific private review separately.

## Grafana

The collector sends credentials only in an in-memory Authorization header to the selected loopback port; it disables proxies and redirects. It checks `/api/health`, `/api/datasources/uid/prometheus`, and `/api/datasources/uid/prometheus/health`. It exports booleans/status only, never credentials or server messages.

In the private UI, confirm the provisioned Prometheus datasource and perform its health test. If API auth/health is unavailable, record NOT VERIFIED and document the UI result separately. View at least one live host metric; an HTTP health endpoint alone does not prove a datasource works.

## Kuma, logs and current boundaries

- Check Kuma through the documented SSH tunnel, verify an approved internal Prometheus readiness monitor, its interval, success history and outage criteria. A setup/login page returning HTTP 200 is not monitor evidence.
- Review the private 30-minute / 200-line-per-container log window. Explain error-like matches and omissions. The collector exports counts only; keywords do not identify cause or prove no errors.
- Confirm actual log driver/rotation, no unexpected privilege or mount changes, secret file access restrictions, effective users/capabilities, host access and firewall/routing intent. Include the Node Exporter exception; cAdvisor stays disabled.
- Record at least two resource/restart observations. Determine whether the restart count increased during the review, distinguish an update from a crash, and state any unobserved history.

## Publication

Copy only reviewed aggregate findings into the summary and timeline. Finish the [sanitisation checklist](../SANITISATION.md), lessons and simulated L2 handoff. No executed result is supplied in this file.
