# Reproducible Compose File Set

This deployment now uses the Compose v2 file set below instead of the previous single `docker-compose.yml` entry point:

- `compose.yaml` for shared services, networks, volumes, private bindings, logging, healthchecks, and optional profiles.
- `compose.lite.yaml` for conservative LITE resource settings.
- `compose.full.yaml` for FULL resource settings and enabling cAdvisor plus AdGuard Home test mode.

Existing named volumes are preserved: `uptime_kuma_data`, `prometheus_data`, `grafana_data`, `adguard_work`, `adguard_conf`, `crowdsec_data`, and `crowdsec_config`.

## LITE command

```bash
cd deploy
cp .env.example .env
$EDITOR .env
./scripts/validate-repository.sh
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml up -d
```

## FULL command

```bash
cd deploy
cp .env.example .env
$EDITOR .env
cp prometheus/cadvisor-target.example.yml prometheus/targets/cadvisor.yml
./scripts/validate-repository.sh
docker compose --env-file .env -f compose.yaml -f compose.full.yaml config
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

cAdvisor and AdGuard Home are optional profiles. CrowdSec remains documentation-only until log acquisition, privacy, and false-positive handling are reviewed. This baseline is a learning environment, not an enterprise SOC or production promise.

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
- CrowdSec has no active Compose service or remediation bouncer in this baseline.
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

The repository is public, but the live homelab is not. Do not place tokens, credentials, private remote URLs, real hostnames, LAN details or operational evidence in commits, shell history, issues or documentation.

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

Edit `.env` locally and replace every `<CHANGE_ME>` value. The real `.env` is ignored by Git and must never be committed. Restrict its permissions according to the host security policy.

Review the rendered configuration before starting containers:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config
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

Optional profiles require a separate review before use.

### Container metrics: `containers`

cAdvisor requires privileged access and sensitive read-only mounts for the host root, runtime state, system data, and Docker data. Review [Docker Container Monitoring](../blue-team-tools/docker-container-monitoring.md) before enabling it.

Activate its Prometheus target and start the profile:

```bash
cp prometheus/cadvisor-target.example.yml prometheus/targets/cadvisor.yml
docker compose --env-file .env -f compose.yaml -f compose.full.yaml up -d
```

The generated target file is ignored by Git. cAdvisor has no published port and is reachable only through the internal `metrics` network.

### DNS security: `dns`

AdGuard Home is a local test service only. It binds the administration interface and test DNS listener to localhost by default:

```bash
docker compose --env-file .env -f compose.yaml -f compose.full.yaml up -d
```

DNS normally uses port 53, but this baseline uses configurable localhost test ports to reduce conflict and exposure. Do not make it the network resolver or point clients at it until availability, privacy, rollback, and LAN design have been reviewed.

### Detection: documentation-only

CrowdSec is intentionally not present as a Compose service. Review `crowdsec/README.md` and `acquis.example.yaml` first. A later change may introduce a `detection` profile only after approved log sources and detection-before-blocking procedures are documented.

## 16. Stop the Stack

Stop and remove the Compose containers and project networks while retaining named volumes:

```bash
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml down
```

Use the FULL file set instead when that mode is running. Do not append `-v` unless the named volumes have been backed up and intentional deletion has been approved.
