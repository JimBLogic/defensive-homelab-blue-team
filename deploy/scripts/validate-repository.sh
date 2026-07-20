#!/usr/bin/env bash
set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
deploy_dir="$repo_root/deploy"
failures=0

pass() { printf 'PASS: %s\n' "$1"; }
fail() { printf 'FAIL: %s\n' "$1" >&2; failures=$((failures + 1)); }
skip() { printf 'SKIPPED — environment unavailable: %s\n' "$1"; }
require_file() {
  [[ -f "$repo_root/$1" ]] \
    && pass "required file exists: $1" \
    || fail "missing required file: $1"
}

required_files=(
  deploy/compose.yaml
  deploy/compose.lite.yaml
  deploy/compose.full.yaml
  deploy/.env.example
  deploy/README.md
  README.md
  SECURITY.md
  docs/lite-vs-full.md
  docs/reproducibility-audit.md
  docs/version-matrix.md
  docs/migration-plan.md
  .gitignore
)
for file in "${required_files[@]}"; do
  require_file "$file"
done

if ! command -v rg >/dev/null 2>&1; then
  fail 'ripgrep (rg) is required for repository validation'
else
  if rg -n ':(latest|main|master)(["[:space:]]|$)' "$repo_root/deploy"; then
    fail 'forbidden broad image tag found'
  else
    pass 'no latest/main/master image tags in deploy'
  fi

  if rg -n ':(.*(alpha|beta|rc|edge|dev|snapshot))' "$repo_root/deploy/.env.example" -i; then
    fail 'pre-release image tag found'
  else
    pass 'no alpha/beta/rc/edge/dev image tags in image variables'
  fi

  if rg -n --pcre2 '\b(jellyfin|jellyseerr|radarr|sonarr|plex|torrent|qbittorrent|transmission)\b' \
    "$repo_root" -i -g '!deploy/scripts/validate-repository.sh'; then
    fail 'forbidden media-stack reference found'
  else
    pass 'no media-stack references found'
  fi

  if rg -n '^\s*(wazuh-manager|wazuh-indexer|wazuh-dashboard):' "$repo_root/deploy"; then
    fail 'forbidden Wazuh central service found'
  else
    pass 'no Wazuh central Docker services found'
  fi

  if rg -n '0\.0\.0\.0:|\[::\]:' \
    "$repo_root/deploy/compose.yaml" \
    "$repo_root/deploy/compose.lite.yaml" \
    "$repo_root/deploy/compose.full.yaml"; then
    fail 'Compose publishes a service on all host interfaces'
  else
    pass 'no all-interface Compose bindings found'
  fi

  if rg -n --pcre2 '^\s*ports:\s*\[\s*"(?!127\.0\.0\.1:)' \
    "$repo_root/deploy/compose.yaml" \
    "$repo_root/deploy/compose.lite.yaml" \
    "$repo_root/deploy/compose.full.yaml"; then
    fail 'inline Compose port binding is not explicitly loopback-only'
  else
    pass 'inline Compose port bindings are loopback-only'
  fi

  if rg -n --pcre2 '^\s*-\s*"(?!127\.0\.0\.1:)[^"/]*:[0-9]+(?:/(?:tcp|udp))?"\s*$' \
    "$repo_root/deploy/compose.yaml" \
    "$repo_root/deploy/compose.lite.yaml" \
    "$repo_root/deploy/compose.full.yaml"; then
    fail 'multiline Compose port binding is not explicitly loopback-only'
  else
    pass 'multiline Compose port bindings are loopback-only'
  fi

  if rg -n --pcre2 -g '!deploy/scripts/validate-repository.sh' -- \
    '-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|ASIA[0-9A-Z]{16}|gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|tailscale.*(tskey|authkey)|password\s*=\s*[^<\s][^\s]+' \
    "$repo_root"; then
    fail 'possible committed secret found'
  else
    pass 'no obvious private keys, cloud keys, tokens, Tailscale keys, or literal passwords found'
  fi
fi

if git -C "$repo_root" check-ignore -q deploy/.env; then
  pass 'deploy/.env is ignored'
else
  fail 'deploy/.env is not ignored'
fi

if grep -Eq '^GRAFANA_ADMIN_PASSWORD=<CHANGE_ME_[A-Z0-9_]+>$' "$deploy_dir/.env.example"; then
  pass 'Grafana example password is an explicit change-me placeholder'
else
  fail 'Grafana example password must remain an explicit <CHANGE_ME_...> placeholder'
fi

for var in \
  UPTIME_KUMA_IMAGE \
  PROMETHEUS_IMAGE \
  NODE_EXPORTER_IMAGE \
  GRAFANA_IMAGE \
  CADVISOR_IMAGE \
  ADGUARD_HOME_IMAGE \
  CROWDSEC_IMAGE; do
  if grep -q "^$var=" "$deploy_dir/.env.example"; then
    pass "image variable exists: $var"
  else
    fail "missing image variable: $var"
  fi
done

if [[ -f "$deploy_dir/compose.yaml" \
  && -f "$deploy_dir/compose.lite.yaml" \
  && -f "$deploy_dir/compose.full.yaml" ]]; then
  pass 'LITE and FULL compose paths exist'
else
  fail 'compose paths missing'
fi

sensitive_tracked=0
while IFS= read -r tracked_file; do
  case "$tracked_file" in
    .env|*/.env|*.ovpn|*.pcap|*.pcapng|*.key|*.pem|*.p12|*.pfx|*.kdbx|*.sqlite|*.sqlite3|*/logs/*|*/backups/*|*/screenshots/*)
      case "$tracked_file" in
        *.example|*.example.*|*/.gitkeep) ;;
        *)
          fail "sensitive runtime or evidence file is tracked: $tracked_file"
          sensitive_tracked=$((sensitive_tracked + 1))
          ;;
      esac
      ;;
  esac
done < <(git -C "$repo_root" ls-files)
if (( sensitive_tracked == 0 )); then
  pass 'no sensitive runtime, packet-capture, key, database, backup, log, or screenshot files are tracked'
fi

while IFS= read -r -d '' script; do
  relative="${script#"$repo_root"/}"
  if head -n1 "$script" | grep -Eq '^#!/usr/bin/env bash$|^#!/bin/bash$'; then
    pass "bash shebang: $relative"
  else
    fail "invalid shebang: $relative"
  fi
  if bash -n "$script"; then
    pass "bash syntax: $relative"
  else
    fail "bash syntax failed: $relative"
  fi
done < <(find "$repo_root" -path '*/.git' -prune -o -name '*.sh' -print0)

if command -v ruby >/dev/null 2>&1; then
  ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f, aliases: true); puts "PASS: YAML parses: #{f}" }' \
    "$repo_root/deploy/compose.yaml" \
    "$repo_root/deploy/compose.lite.yaml" \
    "$repo_root/deploy/compose.full.yaml" \
    "$repo_root/deploy/prometheus/prometheus.yml" \
    "$repo_root/deploy/grafana/provisioning/datasources/prometheus.yml" \
    || fail 'YAML parsing failed'
elif command -v python3 >/dev/null 2>&1; then
  python3 - "$repo_root" <<'PY' || fail 'YAML parsing failed'
import pathlib
import sys

try:
    import yaml
except Exception:
    print('SKIPPED — environment unavailable: PyYAML is not installed')
    raise SystemExit(0)

root = pathlib.Path(sys.argv[1])
for relative in [
    'deploy/compose.yaml',
    'deploy/compose.lite.yaml',
    'deploy/compose.full.yaml',
    'deploy/prometheus/prometheus.yml',
    'deploy/grafana/provisioning/datasources/prometheus.yml',
]:
    yaml.safe_load((root / relative).read_text())
    print(f'PASS: YAML parses: {relative}')
PY
else
  skip 'YAML parser unavailable'
fi

if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  if (cd "$deploy_dir" && docker compose --env-file .env.example -f compose.yaml -f compose.lite.yaml config >/dev/null); then
    pass 'Compose renders for LITE'
  else
    fail 'Compose LITE render failed'
  fi
  if (cd "$deploy_dir" && docker compose --env-file .env.example -f compose.yaml -f compose.full.yaml config >/dev/null); then
    pass 'Compose renders for FULL'
  else
    fail 'Compose FULL render failed'
  fi
else
  skip 'Docker Compose unavailable; LITE/FULL render not executed'
fi

if (( failures > 0 )); then
  printf 'Validation failed with %s issue(s).\n' "$failures" >&2
  exit 1
fi
printf 'Static repository validation completed successfully.\n'
