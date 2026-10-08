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

## Optional-profile safety change

FULL now requires explicit `containers` and `dns` profiles for cAdvisor and AdGuard Home; `detection` remains disabled. Older FULL deployments may retain running optional containers after a file update. Inspect locally, explicitly stop unneeded services, and remove the cAdvisor discovery file without deleting volumes. See [the exception record](../security/runtime-exceptions.md). This is a source change; live migration has not been performed here.
