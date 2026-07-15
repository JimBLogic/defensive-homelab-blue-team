# Migration Plan

## What changed

The previous `deploy/docker-compose.yml` was replaced by the Compose v2 file set:

- `deploy/compose.yaml`
- `deploy/compose.lite.yaml`
- `deploy/compose.full.yaml`

## What remains compatible

Named volumes are preserved: `uptime_kuma_data`, `prometheus_data`, `grafana_data`, `adguard_work`, `adguard_conf`, `crowdsec_data`, and `crowdsec_config`. Prometheus and Grafana provisioning paths remain under `deploy/prometheus` and `deploy/grafana/provisioning`.

## Safe migration steps

```bash
cd deploy
./scripts/validate-repository.sh
docker compose --env-file .env -f compose.yaml -f compose.lite.yaml config
docker compose --env-file .env -f compose.yaml -f compose.full.yaml config
```

Back up named volumes before changing modes or image tags. Start LITE first, verify service health, then enable FULL only after checking resource headroom.

## Rollback

Return to the previous Git commit with:

```bash
git checkout <previous_commit>
```

Then render the previous Compose configuration before restarting. Do not use `docker compose down -v` casually; it deletes persistent named volumes and can turn a configuration rollback into data loss.
