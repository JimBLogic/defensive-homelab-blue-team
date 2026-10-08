#!/usr/bin/env bash
set -euo pipefail

deploy_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$deploy_dir"
mode="${1:-lite}"
case "$mode" in lite|full) ;; *) printf 'Usage: preflight-check.sh [lite|full]\n' >&2; exit 2 ;; esac

failures=0

pass() {
  printf 'PASS: %s\n' "$1"
}

fail() {
  printf 'FAIL: %s\n' "$1" >&2
  failures=$((failures + 1))
}

if command -v docker >/dev/null 2>&1; then
  pass "Docker command is installed: $(docker --version)"
else
  fail "Docker is not installed or is not available on PATH"
fi

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  pass "Docker Compose plugin is available: $(docker compose version)"
else
  fail "Docker Compose plugin is unavailable"
fi

if command -v docker >/dev/null 2>&1 && docker info >/dev/null 2>&1; then
  pass "Current user can communicate with the Docker daemon"
else
  fail "Current user cannot communicate with the Docker daemon"
fi

architecture="$(uname -m)"
printf 'INFO: architecture=%s\n' "$architecture"
case "$architecture" in
  aarch64|arm64)
    pass "64-bit ARM architecture detected"
    ;;
  *)
    printf 'WARN: expected a 64-bit ARM Raspberry Pi, detected %s\n' "$architecture" >&2
    ;;
esac

memory_kib="$(awk '/MemTotal/ {print $2}' /proc/meminfo)"
memory_mib=$((memory_kib / 1024))
printf 'INFO: total_memory_mib=%s\n' "$memory_mib"
if (( memory_mib >= 7000 )); then
  pass "Memory is consistent with an 8GB-class host"
else
  printf 'WARN: less than 7000 MiB of memory was detected\n' >&2
fi

disk_available_kib="$(df -Pk "$deploy_dir" | awk 'NR==2 {print $4}')"
disk_available_gib=$((disk_available_kib / 1024 / 1024))
printf 'INFO: checkout_filesystem_available_disk_gib=%s\n' "$disk_available_gib"

required_files=(
  compose.yaml
  prometheus/prometheus.yml
  grafana/provisioning/datasources/prometheus.yml
  .env
)

for required_file in "${required_files[@]}"; do
  if [[ -f "$required_file" ]]; then
    pass "Required file exists: $required_file"
  else
    fail "Required file is missing: $required_file"
  fi
done

if [[ -f .env ]] && grep -Eq '<[^>]+>' .env; then
  fail ".env still contains placeholder credentials"
elif [[ -f .env ]]; then
  pass ".env does not contain known placeholder credentials"
fi

if (( failures == 0 )); then
  if ! docker compose --env-file .env -f compose.yaml -f "compose.$mode.yaml" config --quiet >/dev/null 2>&1; then
    fail 'Docker Compose configuration failed; inspect privately'
    exit 1
  fi
  pass "Docker Compose configuration renders successfully"
  printf 'Preflight checks completed successfully.\n'
else
  printf 'Preflight checks found %s problem(s).\n' "$failures" >&2
  exit 1
fi
