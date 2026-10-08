#!/usr/bin/env python3
"""Semantic source guardrails and offline Markdown link checks, not deployment evidence."""
import ast
import ipaddress
from pathlib import Path
import re
import subprocess
import sys
import urllib.parse

try:
    import yaml
except ImportError:
    print("FAIL: PyYAML is required for semantic source checks.", file=sys.stderr)
    sys.exit(1)

ROOT = Path(__file__).resolve().parents[2]
CORE = {"uptime-kuma", "prometheus", "node-exporter", "grafana"}
OPTIONAL = {"cadvisor": "containers", "adguard-home": "dns", "crowdsec": "detection"}
SECTIONS = ("Detection", "Evidence", "Initial hypothesis", "Analysis", "Timeline", "MITRE ATT&CK",
            "Query", "Classification", "Impact", "Containment / Action", "Escalation decision",
            "L2 handoff", "Lessons learned", "Detection tuning", "Sanitisation")
SENSITIVE = {".evtx", ".etl", ".pcap", ".pcapng", ".cap", ".key", ".pem", ".p12", ".pfx",
             ".sqlite", ".sqlite3", ".db", ".kdbx", ".ovpn", ".log", ".zip", ".tar", ".gz"}
STATUS = "Deployment-ready defensive baseline · operational validation in progress"


def image_pin(image):
    return bool(re.fullmatch(r"[^\s]+(?::v?\d+\.\d+\.\d+[A-Za-z0-9_.-]*|@sha256:[0-9a-f]{64})", image))


def compose_issues(base, full, lite, env):
    issues = []
    if set(base.get("services", {})) != CORE:
        issues.append("core service set changed")
    if set(full.get("services", {})) != CORE | set(OPTIONAL):
        issues.append("FULL service set changed")
    if set(lite.get("services", {})) != CORE:
        issues.append("LITE service set changed")
    for role in sorted(CORE | set(OPTIONAL)):
        service = {**base.get("services", {}).get(role, {}), **full.get("services", {}).get(role, {})}
        if service.get("profiles", []) != ([OPTIONAL[role]] if role in OPTIONAL else []):
            issues.append("profile guard: " + role)
        if "no-new-privileges:true" not in service.get("security_opt", []):
            issues.append("NNP guard: " + role)
        log = service.get("logging", {})
        if log.get("driver") != "json-file" or log.get("options", {}) != {"max-size": "10m", "max-file": "3"}:
            issues.append("log rotation guard: " + role)
        if service.get("privileged", False) != (role == "cadvisor"):
            issues.append("privileged exception guard: " + role)
        if service.get("network_mode") == "host":
            issues.append("host networking guard: " + role)
        if service.get("pid", "") != ("host" if role == "node-exporter" else ""):
            issues.append("PID exception guard: " + role)
        if role in ("node-exporter", "cadvisor") and not service.get("read_only"):
            issues.append("readonly exporter guard: " + role)
        if role in ("node-exporter", "cadvisor", "crowdsec") and service.get("ports"):
            issues.append("exporter/detection port guard: " + role)
        for port in service.get("ports", []):
            good = (isinstance(port, str) and port.startswith("127.0.0.1:")) or (
                isinstance(port, dict) and port.get("host_ip") in ("127.0.0.1", "::1"))
            if not good:
                issues.append("loopback source guard: " + role)
        if service.get("cap_add") or service.get("devices"):
            issues.append("unreviewed capabilities/devices: " + role)
        image = service.get("image", "")
        match = re.fullmatch(r"\$\{([A-Z_]+)\}", image)
        if not match or not image_pin(env.get(match.group(1), "")):
            issues.append("image pin guard: " + role)
        # Host mounts are restricted to the explicit exporter exceptions and provisioning.
        approved = {
            "uptime-kuma": ["uptime_kuma_data:/app/data"],
            "prometheus": ["./prometheus/prometheus.yml:/etc/prometheus/prometheus.yml:ro",
                           "./prometheus/targets:/etc/prometheus/targets:ro", "prometheus_data:/prometheus"],
            "grafana": ["grafana_data:/var/lib/grafana", "./grafana/provisioning:/etc/grafana/provisioning:ro"],
            "node-exporter": ["/:/host:ro,rslave"],
            "cadvisor": ["/:/rootfs:ro", "/var/run:/var/run:ro", "/sys:/sys:ro",
                         "/var/lib/docker:/var/lib/docker:ro"],
            "adguard-home": ["adguard_work:/opt/adguardhome/work", "adguard_conf:/opt/adguardhome/conf"],
            "crowdsec": ["crowdsec_data:/var/lib/crowdsec/data", "crowdsec_config:/etc/crowdsec",
                        "./crowdsec/acquis.example.yaml:/etc/crowdsec/acquis.yaml:ro"],
        }
        if sorted(service.get("volumes", [])) != sorted(approved[role]):
            issues.append("unreviewed volume/mount: " + role)
        for mode, overlay in (("lite", lite), ("full", full)):
            if role not in overlay.get("services", {}):
                continue
            limits = {**service, **overlay["services"][role]}
            if not limits.get("mem_limit") or float(limits.get("cpus", 0)) <= 0 or limits.get("pids_limit", 0) <= 0:
                issues.append("resource limit guard: " + mode + "/" + role)
    if not base.get("networks", {}).get("metrics", {}).get("internal"):
        issues.append("internal metrics network guard")
    return issues


def headings(text):
    counts = {}
    result = set()
    for line in text.splitlines():
        match = re.match(r"^#{1,6}\s+(.+?)\s*#*\s*$", line)
        if not match:
            continue
        slug = re.sub(r"[^\w\- ]", "", match.group(1).lower()).replace(" ", "-")
        n = counts.get(slug, 0)
        result.add(slug + (f"-{n}" if n else ""))
        counts[slug] = n + 1
    return result


def markdown_link_issues(root):
    issues = []
    for path in root.rglob("*.md"):
        if ".git" in path.parts:
            continue
        text = path.read_text()
        # Check repository-relative Markdown destinations; external URLs require separate review.
        for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
            target = target.strip().split(" ", 1)[0].strip("<>")
            parsed = urllib.parse.urlsplit(target)
            if parsed.scheme or target.startswith("//") or not target:
                continue
            resolved = (path.parent / urllib.parse.unquote(parsed.path)).resolve()
            if not resolved.is_relative_to(root.resolve()) or not resolved.exists():
                issues.append("broken/outside local link: " + path.relative_to(root).as_posix())
            elif parsed.fragment and resolved.is_file() and resolved.suffix == ".md":
                if urllib.parse.unquote(parsed.fragment) not in headings(resolved.read_text()):
                    issues.append("broken local anchor: " + path.relative_to(root).as_posix())
    return issues


def evidence_address_issues(root):
    issues = []
    for path in (root / "exercises").rglob("*.md"):
        # Source references and loopback examples are allowed; actual host addresses are not.
        for value in re.findall(r"(?<![\w.])(?:\d{1,3}\.){3}\d{1,3}(?![\w.])", path.read_text()):
            try:
                address = ipaddress.ip_address(value)
            except ValueError:
                continue
            if not address.is_loopback:
                issues.append("identifying address in exercise: " + path.relative_to(root).as_posix())
    return issues


def operational_link_issues(root):
    issues = []
    text = (root / "README.md").read_text()
    if "\n## Operational evidence\n" not in text:
        return ["Operational evidence section missing"]
    section = text.split("\n## Operational evidence\n", 1)[1].split("\n## ", 1)[0]
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", section):
        path = (root / urllib.parse.urlsplit(target).path).resolve()
        if not path.is_relative_to((root / "exercises").resolve()) or not path.is_file():
            issues.append("Operational evidence must link to an exercise report")
        elif not re.search(r"^\*\*Status:\s*COMPLETED\b", path.read_text(), re.M):
            issues.append("Operational evidence link is not marked COMPLETED")
    return issues


def validate(root=ROOT):
    issues = []
    deploy = root / "deploy"
    files = {name: yaml.safe_load((deploy / name).read_text()) for name in (
        "compose.yaml", "compose.lite.yaml", "compose.full.yaml")}
    env = dict(line.split("=", 1) for line in (deploy / ".env.example").read_text().splitlines()
               if line and not line.startswith("#") and "=" in line)
    issues += compose_issues(files["compose.yaml"], files["compose.full.yaml"], files["compose.lite.yaml"], env)
    for path in root.rglob("*.py"):
        if ".git" not in path.parts:
            try:
                ast.parse(path.read_text())
            except SyntaxError:
                issues.append("Python syntax: " + path.relative_to(root).as_posix())
    issues += markdown_link_issues(root)
    issues += evidence_address_issues(root)
    issues += operational_link_issues(root)
    for name in ["_investigation-template.md", "001-baseline-health-review/README.md",
                 "002-authentication-triage/README.md", "003-process-or-powershell-investigation/README.md",
                 "004-network-dns-investigation/README.md", "005-detection-rule-tuning/README.md"]:
        path = root / "exercises" / name
        if not path.is_file():
            issues.append("missing investigation file: " + name)
            continue
        text = path.read_text()
        for section in SECTIONS:
            if "\n## " + section + "\n" not in text:
                issues.append("missing case section: " + name + "/" + section)
        if name != "_investigation-template.md" and not re.search(
                r"^\*\*Status:\s*(PLANNED|IN PROGRESS|COMPLETED)\b", text, re.M):
            issues.append("case status missing or ambiguous: " + name)
    if STATUS not in (root / "README.md").read_text():
        issues.append("README status statement missing")
    # Do not accept raw binary/runtime evidence even if force-added past .gitignore.
    result = subprocess.run(["git", "-C", str(root), "ls-files", "-z"], capture_output=True, check=True)
    for raw_path in result.stdout.decode().split("\0"):
        if not raw_path:
            continue
        path = Path(raw_path)
        if path.suffix.lower() in SENSITIVE and ".example" not in path.name:
            issues.append("sensitive tracked file: " + raw_path)
        if path.name.startswith(".env") and path.name != ".env.example":
            issues.append("environment file tracked: " + raw_path)
        if raw_path.startswith("exercises/") and path.suffix != ".md":
            issues.append("non-Markdown exercise artifact tracked: " + raw_path)
    return issues


if __name__ == "__main__":
    try:
        failures = validate()
    except (OSError, ValueError, TypeError, KeyError, yaml.YAMLError, subprocess.SubprocessError):
        print("FAIL: semantic source validation could not run; inspect privately.", file=sys.stderr)
        sys.exit(1)
    for failure in sorted(set(failures)):
        print("FAIL: " + failure, file=sys.stderr)
    if failures:
        sys.exit(1)
    print("PASS: semantic Compose/security guards, Python syntax, case structure and local Markdown links")
