# Lessons learned — Exercise 001

**Live operational lessons: pending.**

## Preparation findings actually observed

- The previous FULL configuration started cAdvisor and AdGuard Home without profiles although deployment text described them as disabled. They now require explicit `containers` / `dns` profiles. Existing running instances still need local review; a source change is not proof they stopped.
- The cAdvisor mount of `/var/run` can expose Docker control sockets. The earlier “no Docker socket is mounted” comment was not defensible. [EX-002](../../security/runtime-exceptions.md) now documents this risk and keeps the service off by default.
- The existing preflight placeholder check missed `<CHANGE_ME_LONG_RANDOM_PASSWORD>`. It now checks any angle-bracket placeholder without printing its value.
- The old verifier covered basic running/HTTP checks only. A working datasource, recent scrape, configured Kuma monitor, log review and restart delta need additional observations.
- This editing environment has no Docker/daemon or live lab connection. The evidence register remains NOT VERIFIED.

These are repository-review lessons, not claims of operating or resolving incidents on the Raspberry Pi.

## After the real review

Add what was observed, the evidence ID, why it mattered, competing explanation, actual correction if any, verification and one concrete next improvement. Keep unknowns visible. Do not fill this section with a fictional successful run or an invented incident.
