# Evidence summary — Exercise 001

**Status: NOT VERIFIED — no live homelab evidence collected.**

This is a result register awaiting actual observations, not a sample successful run. The current static validation record belongs to [repository validation](../../docs/validation-2026-10-08.md).

| Evidence ID | Required observation | Current result | How to verify |
| --- | --- | --- | --- |
| BH-01 | Docker daemon and selected Compose mode | NOT VERIFIED | Local daemon access and rendered mode; never publish rendered configuration. |
| BH-02 | Four expected services and unexpected project services | NOT VERIFIED | Running states; account for missing/extra/duplicate containers. |
| BH-03 | Docker health / readiness | NOT VERIFIED | Three configured healthchecks; Node Exporter via successful, fresh scrape. |
| BH-04 | Actual localhost-only bindings | NOT VERIFIED | Inspect runtime bindings, including IPv6; privately inspect host listeners and routing/firewall. |
| BH-05 | Prometheus targets | NOT VERIFIED | Exactly the approved jobs, up and recently scraped. Extra targets require explanation. |
| BH-06 | Grafana datasource | NOT VERIFIED | Configured UID/type/URL and authenticated health request or private UI test. |
| BH-07 | Node Exporter | NOT VERIFIED | Host CPU/memory/filesystem metrics present; rootfs/PID exception reviewed. |
| BH-08 | Uptime Kuma | NOT VERIFIED | HTTP readiness plus actual approved monitor, interval and history. |
| BH-09 | CPU/memory / OOM | NOT VERIFIED | Numeric samples, host trends and capacity rationale; no host labels. |
| BH-10 | Restarts | NOT VERIFIED | Two cumulative observations, elapsed time and explained delta. |
| BH-11 | Disk capacity | NOT VERIFIED | Actual Docker and metrics-volume filesystem free capacity and retention headroom. |
| BH-12 | Logging | NOT VERIFIED | Runtime json-file rotation and bounded private log review; counts are not a full analysis. |
| BH-13 | Current security boundaries | NOT VERIFIED | Secrets permissions, actual ports/mounts, NNP, host access and effective privileges. |
| BH-14 | Optional services | NOT VERIFIED | cAdvisor/DNS/detection off unless explicitly reviewed; legacy FULL instances checked. |

## Results to record after execution

Record collection window (UTC or consistent relative times), repository/tool checksum, authorized environment role, actual check status and aggregate values, observation versus hypothesis, finding/action IDs and private evidence retention role. Remove unused placeholders before completion.

For each failure, state observed impact, supporting evidence, explanation confidence, corrective action **actually taken**, and verification after the action. For each unavailable check, preserve NOT VERIFIED and explain what access/source is missing. Do not convert absence of data into a pass.

## Limits and review

No live screenshots, addresses, users, private domains, labels, DNS history or raw logs have been published. Automated collector checks cannot establish SSH/firewall correctness, a working Kuma monitor, effective least privilege, a backup restore or long-term reliability. The exercise stays incomplete until its mandatory live and manual checks have been reviewed.
