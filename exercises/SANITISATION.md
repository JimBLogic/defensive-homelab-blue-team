# Evidence handling and sanitisation

Private originals and public summaries have different purposes. Keep originals in protected storage **outside the checkout**; do not upload raw evidence to CI artifacts, issues or a pull request. The health collector deliberately publishes only a small allowlist of service roles, enums, booleans, numeric aggregates, UTC collection time and repository/tool checksums. It never dumps raw command/API results or exception strings.

## Publication checklist

- [ ] Record whether this is observed homelab activity, an approved simulation, a synthetic fixture or repository validation.
- [ ] Keep real public/private addresses, hostnames, usernames, domains, DNS history, topology, credentials, tokens, environment values and private paths out.
- [ ] Use stable placeholders such as `<HOST_A>`, `<ACCOUNT_A>`, `<DOMAIN_A>` and `<EVIDENCE_A>`; keep any lookup table private.
- [ ] Prefer totals/percentages and a written finding over copied log lines. Do not publish a command line that contains an identifier or secret.
- [ ] Preserve chronological order; use UTC or consistently shifted relative times. State any transformation and avoid fabricated timestamps.
- [ ] Review API errors, scrape labels, process trees, browser tabs, notification targets and terminal prompts for leaks.
- [ ] Do not publish raw captures, EVTX, databases, screenshots, archives, rendered Compose or `docker inspect` output.
- [ ] Human-review the minimized report: allowlisted numbers can still reveal capacity or activity. Further aggregate or omit if needed.
- [ ] State remaining evidence gaps and retain enough query/method context for review without leaking the private environment.
- [ ] Run repository validation, examine `git diff --cached` and explicitly stage only reviewed Markdown summaries.

The collector report is **not automatically approved for publication**. Copy only necessary, reviewed facts into `evidence-summary.md` and the investigation. A checksum of collector code helps reproducibility; it does not attest to honesty or establish forensic chain of custody. A report from this editing environment is not evidence of operating the Raspberry Pi.

See [SECURITY.md](../SECURITY.md) for accidental disclosure response. Automated pattern checks supplement human review and cannot prove that evidence is safe.
