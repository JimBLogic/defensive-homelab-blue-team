# Reproducible Compose File Set

**Deployment-ready defensive baseline · operational validation in progress**

This guide describes configured behavior. No live deployment has been verified in the published exercises.

This deployment now uses the Compose v2 file set below instead of the previous single `docker-compose.yml` entry point:

- `compose.yaml` for shared services, networks, volumes, private bindings, logging, healthchecks, and optional profiles.
- `compose.lite.yaml` for conservative LITE resource settings.
- `compose.full.yaml` for FULL resource settings; optional services still require explicit profiles.

Existing named volumes are preserved: `uptime_kuma_data`, `prometheus_data`, `grafana_data`, `adguard_work`, `adguard_conf`, `crowdsec_data`, and `crowdsec_config`.

## LITE command

```bash
cd deploy
cp .env.example .env
$EDITOR .env
./scripts/validate-repository.sh
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config --quiet
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml up -d
```

## FULL command

```bash
cd deploy
cp .env.example .env
$EDITOR .env
./scripts/validate-repository.sh
docker compose --env-file .env -f compose.yaml -f compose.full.yaml config --quiet
docker compose --env-file .env -f compose.yaml -f compose.full.yaml up -d
```

Do not use `docker compose down -v` casually because it deletes persistent named volumes. Return to the previous deployment by checking out the previous Git commit and rendering the configuration before restart.

---

# Raspberry Pi 4 Blue Team Docker Baseline

## 1. Purpose

This directory provides the first testable Docker baseline for the Defensive Homelab Blue Team Lab. It is designed for controlled learning on a Raspberry Pi 4 and starts only four services by default:

- Uptime Kuma for availability checks.
- Prometheus for metrics collection.
- Node Exporter for Linux host metrics.
- Grafana OSS for dashboards.

cAdvisor and AdGuard Home require explicit `containers` and `dns` profiles. CrowdSec is defined only in FULL behind the disabled `detection` profile; acquisition and alert handling remain unvalidated. No optional service is needed for Exercise 001.

## 2. Hardware Assumptions

- Raspberry Pi 4 with 8GB RAM.
- 64-bit Linux operating system supported by Docker.
- 1TB SSD mounted and tested by the operator.
- Reliable power and wired networking where practical.

The deployment does not assume a particular SSD device name, filesystem, or mount path. Use a placeholder such as `<SSD_MOUNT_POINT>` in notes and adapt storage decisions to the actual host. Nothing in this repository formats or repartitions storage.

## 3. Security Model

- Uptime Kuma, Prometheus, and Grafana bind to `127.0.0.1` by default.
- Dashboards are accessed from `<ADMIN_WORKSTATION>` through SSH port forwarding.
- Node Exporter and cAdvisor have no published host ports; Prometheus reaches them through the internal `metrics` network.
- cAdvisor is disabled by default because it requires sensitive read-only host mounts and privileged access.
- AdGuard Home is disabled by default and binds its test DNS and administration ports to localhost.
- CrowdSec remains disabled behind the `detection` profile, with no remediation bouncer or validated log acquisition.
- Real credentials, addresses, hostnames, logs, and environment values remain outside Git.

## 4. Prerequisites

- A maintained 64-bit Raspberry Pi Linux installation.
- Docker Engine installed from trusted, official guidance.
- Docker Compose v2 plugin.
- Git for retrieving the repository.
- SSH access from `<ADMIN_WORKSTATION>` if dashboards will be viewed remotely.
- An operator-approved SSD mount with enough free space for metrics retention and backups.

Do not use unreviewed external installation scripts. Confirm package sources and installation instructions for the chosen operating system.

## 5. Recommended Host Preparation

Before deployment:

1. Apply reviewed operating-system updates and reboot if required.
2. Confirm system time synchronization.
3. Confirm the SSD is mounted at the intended `<SSD_MOUNT_POINT>` and survives a planned reboot.
4. Review free disk space, filesystem health, memory, temperature, and power stability.
5. Confirm the administrative account can run Docker without exposing the Docker API.
6. Decide where encrypted or access-controlled backups will be stored as `<BACKUP_TARGET>`.

This guide does not format disks, change firewall rules, or alter SSH configuration.

## 6. Docker and Compose Verification

Run these read-only version checks:

```bash
docker --version
docker compose version
```

After the repository and `.env` are prepared, the included preflight script checks Docker access, architecture, memory, disk space, required files, placeholders, and Compose rendering:

```bash
./scripts/preflight-check.sh
```

## 7. Repository Setup

Clone the public repository over HTTPS or SSH using GitHub's standard methods:

```bash
git clone https://github.com/JimBLogic/defensive-homelab-blue-team.git
cd defensive-homelab-blue-team/deploy
```

The repository is public, but the live homelab is not. Do not place tokens, credentials, private remote URLs, real hostnames, LAN details or raw/identifying operational evidence in commits, shell history, issues or documentation.

Before publishing a branch, run:

```bash
./scripts/validate-repository.sh
```

The validator checks tracked filenames, common secret patterns, Compose bindings, image tags, placeholders and repository syntax. It is a guardrail, not proof that a commit contains no sensitive information; review the full diff manually as well.

## 8. Environment File Setup

If `.env` does not already exist, create it from the safe example:

```bash
cp .env.example .env
```

Edit `.env` locally and replace every angle-bracket placeholder, including `<CHANGE_ME_LONG_RANDOM_PASSWORD>`. The real `.env` is ignored by Git and must never be committed. Restrict its permissions according to the host security policy.

Review the rendered configuration before starting containers:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config --quiet
```

The example uses explicit candidate image pins from `.env.example`. Verify ARM64 manifests on the Raspberry Pi before claiming runtime compatibility.

## 9. Start the Default Stack

Run the preflight check, then start only the default services:

```bash
./scripts/preflight-check.sh
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml up -d
```

No optional profile is enabled by this command.

## 10. Verify Running Containers

Review service state and recent logs:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml ps
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml logs --tail=50
./scripts/verify-stack.sh
```

Expected default services are `uptime-kuma`, `prometheus`, `node-exporter`, and `grafana`. Treat repeated restarts, unhealthy states, missing metrics, or unexpected errors as findings to investigate.

## 11. Access Dashboards Safely Through SSH Tunnels

From `<ADMIN_WORKSTATION>`, create one tunnel per dashboard as needed:

```bash
ssh -L 3001:127.0.0.1:3001 <USER>@<HOMELAB_HOST>
ssh -L 9090:127.0.0.1:9090 <USER>@<HOMELAB_HOST>
ssh -L 3000:127.0.0.1:3000 <USER>@<HOMELAB_HOST>
```

While the appropriate tunnel is open, use:

- Uptime Kuma: `http://127.0.0.1:3001`
- Prometheus: `http://127.0.0.1:9090`
- Grafana: `http://127.0.0.1:3000`

These are loopback addresses, not real infrastructure values. Do not change the Compose bindings to LAN-wide or public addresses without a separate exposure review.

## 12. First Uptime Kuma Check

1. Open Uptime Kuma through the SSH tunnel.
2. Create the initial administrator account with a strong local credential stored outside Git.
3. Add one Docker-internal HTTP check for `http://prometheus:9090/-/ready`.
4. Use a sanitized display name such as `<SERVICE_NAME>`.
5. Record the expected state, check interval, and what duration would count as an incident.

Do not add real public targets or copy notification secrets into this repository.

## 13. First Prometheus Check

Open Prometheus through the SSH tunnel and review the Targets page. The default configuration should show:

- `prometheus:9090` for Prometheus self-monitoring.
- `node-exporter:9100` for host metrics.

cAdvisor should not appear until its reviewed target file is enabled with the `containers` profile. Record any failed scrape without publishing host labels or raw operational data.

## 14. First Grafana Check

1. Open Grafana through the SSH tunnel.
2. Sign in with the local credentials configured in `.env`.
3. Confirm the provisioned Prometheus datasource reports successfully.
4. Create a minimal dashboard for CPU, memory, filesystem, and service-health investigation.
5. Keep dashboard labels sanitized and do not publish screenshots yet.

## 15. Optional Profiles

FULL alone keeps all optional profiles disabled. Review [runtime exceptions](../security/runtime-exceptions.md) before any activation. Existing containers from an older FULL revision may remain running; inspect them privately and explicitly stop unwanted services without deleting volumes.

### Container metrics: `containers` — high-risk exception

Not needed for Exercise 001. cAdvisor retains privileged mode and broad host mounts. `/var/run:ro` may expose the Docker socket; read-only does not limit socket API permissions. Necessity of privileged mode on this host is unverified. Only after a separate privilege/resource/privacy review:

```bash
cp prometheus/cadvisor-target.example.yml prometheus/targets/cadvisor.yml
docker compose --env-file .env -f compose.yaml -f compose.full.yaml --profile containers up -d
```

The target file is ignored by Git. cAdvisor publishes no host port. Stop and remove its discovery file as described in EX-002 when no longer needed; do not claim an internal network eliminates the privilege risk.

### DNS security: `dns`

AdGuard Home is for localhost test DNS and administration, not the LAN resolver. Only after a separate privacy/capacity review:

```bash
docker compose --env-file .env -f compose.yaml -f compose.full.yaml --profile dns up -d
```

Do not point home clients at it, collect browsing histories, or replace DNS settings for this exercise.

### Detection: `detection` — planned, disabled

A disabled CrowdSec definition exists in FULL. Review `crowdsec/README.md` and `acquis.example.yaml` before even a test deployment. No approved acquisition source or detection/remediation result exists. There is no bouncer; use the single Windows/Sysmon → external Wazuh path for the first SOC investigations.

## 16. Stop the Stack

Stop and remove the Compose containers and project networks while retaining named volumes:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml down
```

Use the FULL file set instead when that mode is running. Do not append `-v` unless the named volumes have been backed up and intentional deletion has been approved.

## 17. Update Workflow

1. Read upstream release notes and security notices.
2. Back up required configuration and named-volume data.
3. Change one image tag or logical service group at a time.
4. Render the configuration and review the diff.
5. Pull the reviewed images, recreate services, and verify health.
6. Record the validated versions and rollback decision.

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config --quiet
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml pull
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml up -d
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml ps
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml logs --tail=50
```

## 18. Backup Notes

The default stack stores persistent state in named volumes:

- `uptime_kuma_data`
- `prometheus_data`
- `grafana_data`

The optional DNS profile adds `adguard_work` and `adguard_conf`. Inspect volume metadata with `docker volume inspect <VOLUME_NAME>` and design a backup method that produces a consistent copy at `<BACKUP_TARGET>`.

Do not commit volume data, database contents, archives, `.env`, dashboard credentials, or raw logs. A backup is not considered valid until an isolated restore test succeeds.

## 19. Troubleshooting

Start with read-only status and configuration checks:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config --quiet
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml ps
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml logs --tail=50 <SERVICE_NAME>
ss -lnt
df -h
free -h
```

Common review questions:

- Does `.env` still contain `<CHANGE_ME>`?
- Is another local process using the selected loopback port?
- Is the service repeatedly restarting?
- Can Prometheus resolve the Docker service name?
- Does the SSD have sufficient free space?
- Did a recent image or configuration change introduce the failure?

Keep troubleshooting notes sanitized and avoid pasting raw logs into Git.

## 20. Operational Exercise 001 — Baseline Service Health Review

**IN PROGRESS / NOT VERIFIED.** The authoritative procedure, completion criteria, evidence register and lessons are in [Exercise 001](../exercises/001-baseline-health-review/README.md).

```bash
./scripts/verify-stack.sh lite
python3 scripts/baseline-health-review.py --mode lite --output /tmp/baseline-health-review.json
```

Use `full` for the actually deployed FULL mode. The collector is read-only and keeps manual checks pending. Run a second observation after at least five minutes, review private logs/Kuma/SSH/firewall/storage/effective privileges, then write a human-reviewed sanitized result. An unavailable check is not a pass. No live operational exercise has been completed in this repository yet.
