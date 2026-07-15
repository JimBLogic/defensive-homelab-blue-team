#!/usr/bin/env bash
set -euo pipefail
repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
deploy_dir="$repo_root/deploy"
failures=0
pass(){ printf 'PASS: %s\n' "$1"; }
fail(){ printf 'FAIL: %s\n' "$1" >&2; failures=$((failures+1)); }
skip(){ printf 'SKIPPED — environment unavailable: %s\n' "$1"; }
require_file(){ [[ -f "$repo_root/$1" ]] && pass "required file exists: $1" || fail "missing required file: $1"; }
for f in deploy/compose.yaml deploy/compose.lite.yaml deploy/compose.full.yaml deploy/.env.example deploy/README.md README.md docs/lite-vs-full.md docs/reproducibility-audit.md docs/version-matrix.md docs/migration-plan.md .gitignore; do require_file "$f"; done
if rg -n ':(latest|main|master)(["[:space:]]|$)' "$repo_root/deploy"; then fail 'forbidden broad image tag found'; else pass 'no latest/main/master image tags in deploy'; fi
if rg -n ':(.*(alpha|beta|rc|edge|dev|snapshot))' "$repo_root/deploy/.env.example" -i; then fail 'pre-release image tag found'; else pass 'no alpha/beta/rc/edge/dev image tags in image variables'; fi
if rg -n --pcre2 '\b(jellyfin|jellyseerr|radarr|sonarr|plex|torrent|qbittorrent|transmission)\b' "$repo_root" -i -g '!deploy/scripts/validate-repository.sh'; then fail 'forbidden media-stack reference found'; else pass 'no media-stack references found'; fi
if rg -n '^\s*(wazuh-manager|wazuh-indexer|wazuh-dashboard):' "$repo_root/deploy"; then fail 'forbidden Wazuh central service found'; else pass 'no Wazuh central Docker services found'; fi
if rg -n '0\.0\.0\.0:.*(3000|3001|9090|3002)' "$repo_root/deploy"; then fail 'dashboard bound to all interfaces'; else pass 'no all-interface dashboard bindings found'; fi
if git -C "$repo_root" check-ignore -q deploy/.env; then pass 'deploy/.env is ignored'; else fail 'deploy/.env is not ignored'; fi
for var in UPTIME_KUMA_IMAGE PROMETHEUS_IMAGE NODE_EXPORTER_IMAGE GRAFANA_IMAGE CADVISOR_IMAGE ADGUARD_HOME_IMAGE CROWDSEC_IMAGE; do grep -q "^$var=" "$deploy_dir/.env.example" && pass "image variable exists: $var" || fail "missing image variable: $var"; done
if [[ -f "$deploy_dir/compose.yaml" && -f "$deploy_dir/compose.lite.yaml" && -f "$deploy_dir/compose.full.yaml" ]]; then pass 'LITE and FULL compose paths exist'; else fail 'compose paths missing'; fi
while IFS= read -r -d '' script; do head -n1 "$script" | grep -Eq '^#!/usr/bin/env bash$|^#!/bin/bash$' && pass "bash shebang: ${script#$repo_root/}" || fail "invalid shebang: ${script#$repo_root/}"; bash -n "$script" && pass "bash syntax: ${script#$repo_root/}" || fail "bash syntax failed: ${script#$repo_root/}"; done < <(find "$repo_root" -path '*/.git' -prune -o -name '*.sh' -print0)
if rg -n --pcre2 -g '!deploy/scripts/validate-repository.sh' -- '-----BEGIN (RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----|AKIA[0-9A-Z]{16}|tailscale.*(tskey|authkey)|password\s*=\s*[^<\s][^\s]+' "$repo_root"; then fail 'possible committed secret found'; else pass 'no obvious private keys, cloud keys, Tailscale keys, or literal passwords found'; fi
if command -v ruby >/dev/null 2>&1; then
  ruby -e 'require "yaml"; ARGV.each { |f| YAML.load_file(f, aliases: true); puts "PASS: YAML parses: #{f}" }' \
    "$repo_root/deploy/compose.yaml" \
    "$repo_root/deploy/compose.lite.yaml" \
    "$repo_root/deploy/compose.full.yaml" \
    "$repo_root/deploy/prometheus/prometheus.yml" \
    "$repo_root/deploy/grafana/provisioning/datasources/prometheus.yml" || fail 'YAML parsing failed'
elif command -v python3 >/dev/null 2>&1; then
  python3 - <<'PY' "$repo_root" || exit 1
import pathlib, sys
try:
 import yaml
except Exception:
 print('SKIPPED — environment unavailable: PyYAML is not installed')
 sys.exit(0)
root=pathlib.Path(sys.argv[1])
for rel in ['deploy/compose.yaml','deploy/compose.lite.yaml','deploy/compose.full.yaml','deploy/prometheus/prometheus.yml','deploy/grafana/provisioning/datasources/prometheus.yml']:
 yaml.safe_load((root/rel).read_text())
 print(f'PASS: YAML parses: {rel}')
PY
else skip 'YAML parser unavailable'; fi
if command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
  (cd "$deploy_dir" && docker compose --env-file .env.example -f compose.yaml -f compose.lite.yaml config >/dev/null) && pass 'Compose renders for LITE' || fail 'Compose LITE render failed'
  (cd "$deploy_dir" && docker compose --env-file .env.example -f compose.yaml -f compose.full.yaml config >/dev/null) && pass 'Compose renders for FULL' || fail 'Compose FULL render failed'
else
  skip 'Docker Compose unavailable; LITE/FULL render not executed'
fi
if (( failures > 0 )); then printf 'Validation failed with %s issue(s).\n' "$failures" >&2; exit 1; fi
printf 'Static repository validation completed successfully.\n'
