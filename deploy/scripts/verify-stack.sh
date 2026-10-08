#!/usr/bin/env bash
set -euo pipefail

deploy_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$deploy_dir"
mode="${1:-lite}"
case "$mode" in lite|full) ;; *) printf 'Usage: verify-stack.sh [lite|full]\n' >&2; exit 2 ;; esac
compose=(docker compose --env-file .env -f compose.yaml -f "compose.$mode.yaml")
failures=0
pass() { printf 'PASS: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; failures=$((failures + 1)); }

if ! command -v docker >/dev/null 2>&1 || ! docker compose version >/dev/null 2>&1; then
  printf 'NOT VERIFIED: Docker Compose unavailable.\n' >&2
  exit 2
fi
for required in .env compose.yaml "compose.$mode.yaml" prometheus/prometheus.yml grafana/provisioning/datasources/prometheus.yml; do
  [[ -f "$required" ]] || fail "required local file missing: $required"
done
if (( failures > 0 )); then exit 1; fi

# Rendered configuration and command errors may include secrets; suppress both.
if "${compose[@]}" config --quiet >/dev/null 2>&1; then
  pass 'Compose configuration renders'
else
  fail 'Compose configuration does not render; inspect privately'
  exit 1
fi
if ! running_services="$("${compose[@]}" ps --services --filter status=running 2>/dev/null)"; then
  fail 'service state unavailable; inspect privately'
  exit 1
fi
for service in uptime-kuma prometheus node-exporter grafana; do
  if rg -Fxq "$service" <<<"$running_services"; then pass "core service running: $service"
  else fail "core service missing: $service"; fi
done
if command -v curl >/dev/null 2>&1 && command -v python3 >/dev/null 2>&1; then
  # Read resolved public port numbers only; never emit rendered configuration.
  mapfile -t ports < <("${compose[@]}" config --format json 2>/dev/null | python3 -c '
import json, sys
try:
    data=json.load(sys.stdin)
    for role, target in (("uptime-kuma",3001),("prometheus",9090),("grafana",3000)):
        matches=[p for p in data["services"][role].get("ports",[]) if p.get("host_ip")=="127.0.0.1" and p.get("protocol","tcp")=="tcp" and int(p["target"])==target]
        if len(matches)!=1: raise ValueError()
        port=int(matches[0]["published"])
        if not 1 <= port <= 65535: raise ValueError()
        print(port)
except (ValueError, TypeError, KeyError):
    sys.exit(1)
  ' 2>/dev/null)
  if (( ${#ports[@]} != 3 )); then
    fail 'safe endpoint port configuration unavailable'
  else
    roles=(uptime-kuma prometheus grafana)
    paths=(/ /-/ready /api/health)
    for i in 0 1 2; do
      if curl --fail --silent --max-time 5 --noproxy '*' --proto '=http' \
        "http://127.0.0.1:${ports[$i]}${paths[$i]}" >/dev/null 2>&1; then
        pass "local endpoint responded: ${roles[$i]}"
      else
        fail "local endpoint unavailable: ${roles[$i]}"
      fi
    done
  fi
else
  printf 'NOT VERIFIED: HTTP checks require curl and Python 3.\n' >&2
  exit 2
fi
printf 'Basic state/HTTP checks only; health, telemetry, exposure and manual review require Exercise 001.\n'
printf 'Run: python3 scripts/baseline-health-review.py --mode %s --output /tmp/baseline-health-review.json\n' "$mode"
if (( failures > 0 )); then exit 1; fi
