# Runtime privilege and exposure exceptions

**Deployment-ready defensive baseline · operational validation in progress**

These are configuration decisions, not assertions that host hardening has been verified. Revalidate after image, kernel, Docker, cgroup or storage changes. All profiles are off by default. The four core services inherit `no-new-privileges` and rotating JSON logs; image defaults still need an effective user/capability review.

## EX-001 — Node Exporter host visibility

`pid: host` and `/:/host:ro,rslave` support host process/filesystem metrics rather than only container metrics. The root filesystem is read-only inside the container, but host paths and potentially readable sensitive files remain exposed. Shared PID visibility weakens isolation. This is not an ordinary unprivileged application boundary.

No host port is published; Prometheus reaches it on the internal metrics network. Retain the read-only root filesystem, no-new-privileges and resource limits. During 001, confirm the deployed mounts/PID setting match the reviewed configuration and that the target supplies **host** metrics. Do not add capabilities or writable mounts to fix missing metrics without evidence and a separate review. An effective capability/non-root reduction remains pending on-device compatibility testing.

## EX-002 — cAdvisor (high risk; disabled)

cAdvisor is behind the **`containers` profile**, even in FULL. It is unnecessary for baseline health review: `docker inspect` and `docker stats` answer the current questions without adding an exporter.

The existing optional configuration retains `privileged: true` as a compatibility exception for host cgroup/runtime visibility. **Its necessity on this Raspberry Pi/kernel has not been demonstrated.** Upstream documents configurations that need extra privileges and configurations using narrower device/seccomp settings; do not treat privileged mode as an inherent requirement for every host.

| Mount | Intended purpose | Risk |
| --- | --- | --- |
| `/:/rootfs:ro` | Host filesystem accounting | Broad read visibility into host paths and data. |
| `/sys:/sys:ro` | cgroup/system counters | Reveals host device and kernel information. |
| `/var/lib/docker:/var/lib/docker:ro` | Container storage accounting | Exposes runtime/container data and potentially secrets. |
| `/var/run:/var/run:ro` | Runtime metadata/socket discovery | May include `docker.sock` and other control sockets. Read-only filesystem mounts do **not** make Unix-socket API operations read-only. |

Privileged mode greatly weakens container isolation and may allow host compromise if the exporter or image is compromised. `read_only`, `no-new-privileges` and an internal network do not cancel this risk. Docker daemon access is security-critical and commonly equivalent to host administrative control.

Keep it disabled when the learning question can be answered without it, the privilege necessity is untested, the host contains sensitive workloads, the required mounts cannot be justified, the image/architecture is unverified, or the host has insufficient headroom. No bouncer or automatic containment is introduced.

Before a separate cAdvisor exercise, document an operator-reviewed exception with purpose, required metrics, minimum working privileges, private socket/mount review, time limit and rollback. Test narrower privileges on a disposable host first. Do not silently weaken kernel settings or mount new devices. Enable only after that review:

```bash
cd deploy
cp prometheus/cadvisor-target.example.yml prometheus/targets/cadvisor.yml
docker compose --env-file .env -f compose.yaml -f compose.full.yaml --profile containers up -d
```

If already running from an older FULL configuration, changing profiles does not guarantee it has stopped. Check locally. To disable it without removing volumes:

```bash
docker compose --env-file .env -f compose.yaml -f compose.full.yaml --profile containers stop cadvisor
rm -f prometheus/targets/cadvisor.yml
```

After the next target-discovery interval, verify the cAdvisor target is absent. Do not use `down -v`. The collector flags an optional running service when its profile was not selected for the review.

## EX-003 — administrative and host boundaries

Loopback published ports limit network exposure but remain accessible to local users/processes. Container-network peers can also reach service listeners. The internal metrics network is not an authentication boundary. Node Exporter has host visibility; Prometheus/Grafana also join the monitoring network. Confirm actual bindings, unrelated host listeners, Docker API exposure, SSH access, routing/firewall intent, secrets permissions and pending hardening items privately. A Compose check cannot prove the whole host is isolated.

Prometheus retains its existing lifecycle endpoint, reachable within its networks/loopback binding. Treat reload access as administrative access; never expose it broadly. Grafana credentials remain in local runtime configuration, and Docker administrators can inspect container environment values. Keep `.env` access restricted; do not paste rendered Compose or inspection output into public artifacts.

## Primary references

- [Docker Engine security](https://docs.docker.com/engine/security/)
- [cAdvisor upstream runtime guidance](https://github.com/google/cadvisor/blob/master/docs/running.md)

These references explain risk and upstream options; they are not evidence that this deployment was exercised.
