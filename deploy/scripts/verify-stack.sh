#!/usr/bin/env bash
set -euo pipefail

deploy_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$deploy_dir"

failures=0

pass() {
  printf 'PASS: %s\n' "$1"
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

required_files=(
  .env
  docker-compose.yml
  prometheus/prometheus.yml
  grafana/provisioning/datasources/prometheus.yml
)

for required_file in "${required_files[@]}"; do
  if [[ -f "$required_file" ]]; then
    pass "Required file exists: $required_file"
  else
    fail "Required file is missing: $required_file"
  fi
done

if [[ ! -f .env ]]; then
  printf 'Verification cannot continue without .env.\n' >&2
  exit 1
fi

docker compose --env-file .env config >/dev/null
pass "Docker Compose configuration renders successfully"

running_services="$(docker compose --env-file .env ps --services --filter status=running)"
expected_services=(uptime-kuma prometheus node-exporter grafana)

for service in "${expected_services[@]}"; do
  if grep -Fxq "$service" <<<"$running_services"; then
    pass "Default service is running: $service"
  else
    fail "Default service is not running: $service"
  fi
done

env_value() {
  local key="$1"
  local fallback="$2"
  local value
  value="$(sed -n "s/^${key}=//p" .env | tail -n 1)"
  printf '%s' "${value:-$fallback}"
}

if command -v curl >/dev/null 2>&1; then
  uptime_port="$(env_value UPTIME_KUMA_PORT 3001)"
  prometheus_port="$(env_value PROMETHEUS_PORT 9090)"
  grafana_port="$(env_value GRAFANA_PORT 3000)"

  endpoints=(
    "Uptime Kuma|http://127.0.0.1:${uptime_port}/"
    "Prometheus|http://127.0.0.1:${prometheus_port}/-/ready"
    "Grafana|http://127.0.0.1:${grafana_port}/api/health"
  )

  for endpoint in "${endpoints[@]}"; do
    name="${endpoint%%|*}"
    url="${endpoint#*|}"
    if curl --fail --silent --show-error --max-time 5 "$url" >/dev/null; then
      pass "Local endpoint responded: $name"
    else
      fail "Local endpoint did not respond: $name"
    fi
  done
else
  printf 'WARN: curl is unavailable; local endpoint checks were skipped\n' >&2
fi

if (( failures == 0 )); then
  printf 'Default stack verification completed successfully.\n'
else
  printf 'Stack verification found %s problem(s).\n' "$failures" >&2
  exit 1
fi
