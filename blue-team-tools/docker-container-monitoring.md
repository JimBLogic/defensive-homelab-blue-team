# Docker Container Monitoring

## Purpose

Provide visibility into container CPU, memory, network activity, restart behavior, and health status using cAdvisor or a narrower Docker metrics exporter.

## Why It Fits This Homelab

Container visibility connects Docker operations with defensive monitoring and helps identify unstable, noisy, or unexpectedly resource-intensive workloads.

## Defensive Value

- Highlights restart loops and unhealthy services.
- Compares container demand with host resource pressure.
- Supports post-update validation and incident timelines.

## Data Collected

Container identifiers, names or sanitized labels, resource metrics, network counters, restart state, health, and lifecycle information depending on the selected exporter.

## Security Considerations

- Treat the Docker socket as host-sensitive control-plane access.
- Prefer an approach that does not require the raw socket.
- If mounts are necessary, use the narrowest read-only set and document each one.
- Avoid privileged mode, host networking, and unnecessary capabilities.

## Privacy Considerations

Container names, image labels, mounts, and network metadata may reveal architecture. Publish only sanitized summaries.

## Exposure Recommendation

Metrics endpoint: not publicly exposed. Dashboard access: `<LOCAL_ONLY>` or justified `<VPN_ONLY>`.

## Example Use Cases

- Investigate why `<CONTAINER_NAME>` restarted repeatedly.
- Identify a sustained memory increase after an update.
- Compare container health with Uptime Kuma availability.

## TODO / Future Improvements

- [ ] Compare cAdvisor with a narrower exporter for privilege and data needs.
- [ ] Document every required mount and capability before deployment.
- [ ] Define restart and resource review criteria from a normal baseline.
