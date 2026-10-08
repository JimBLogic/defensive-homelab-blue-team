#!/usr/bin/env python3
"""Read-only, minimized health observations. Never closes an exercise."""
import argparse
import base64
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[2]
DEPLOY = ROOT / "deploy"
CORE = ("uptime-kuma", "prometheus", "node-exporter", "grafana")
OPTIONAL = {"cadvisor": "containers", "adguard-home": "dns", "crowdsec": "detection"}
KNOWN = CORE + tuple(OPTIONAL)
STATUSES = {"PASS", "FAIL", "NOT_VERIFIED", "REVIEW_REQUIRED"}
STATES = {"running", "created", "restarting", "removing", "paused", "exited", "dead"}
HEALTH = {"healthy", "unhealthy", "starting", "not-configured"}
TIMEOUT = 20


class Unavailable(Exception):
    """No raw command, URL, stderr or exception details may be published."""


def command(args, *, log_stderr=False, timeout=TIMEOUT):
    try:
        result = subprocess.run(args, cwd=DEPLOY, text=True, capture_output=True,
                                timeout=timeout, check=False)
        if result.returncode:
            raise Unavailable()
        output = result.stdout + (result.stderr if log_stderr else "")
        if len(output) > 4 * 1024 * 1024:
            raise Unavailable()
        return output
    except (OSError, subprocess.SubprocessError, UnicodeError):
        raise Unavailable() from None


def number(value, *, minimum=0, maximum=1e18):
    try:
        value = float(value)
    except (TypeError, ValueError, OverflowError):
        raise Unavailable() from None
    if not math.isfinite(value) or not minimum <= value <= maximum:
        raise Unavailable()
    return round(value, 3)


def integer(value):
    value = number(value)
    if value != int(value):
        raise Unavailable()
    return int(value)


def pin(image):
    return bool(re.fullmatch(r"[^\s]+(?::v?\d+\.\d+\.\d+[A-Za-z0-9_.-]*|@sha256:[0-9a-f]{64})", str(image)))


def loopback(bindings):
    return all(item.get("HostIp") in ("127.0.0.1", "::1")
               for values in (bindings or {}).values() for item in (values or []))


def fresh_scrape(target, now=None):
    try:
        timestamp = datetime.fromisoformat(target.get("lastScrape", "").replace("Z", "+00:00"))
        age = ((now or datetime.now(timezone.utc)) - timestamp).total_seconds()
        return 0 <= age <= 90
    except (ValueError, TypeError):
        return False


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def http(port, path, *, credentials=None, as_json=True):
    # Destination is fixed loopback, with no proxy or redirect credential leakage.
    port = integer(port)
    if not 1 <= port <= 65535 or not path.startswith("/"):
        raise Unavailable()
    request = urllib.request.Request(f"http://127.0.0.1:{port}{path}")
    if credentials is not None:
        token = base64.b64encode((credentials[0] + ":" + credentials[1]).encode()).decode()
        request.add_header("Authorization", "Basic " + token)
    opener = urllib.request.build_opener(urllib.request.ProxyHandler({}), NoRedirect())
    try:
        with opener.open(request, timeout=5) as response:
            data = response.read(2 * 1024 * 1024 + 1)
            if len(data) > 2 * 1024 * 1024:
                raise Unavailable()
            return json.loads(data) if as_json else response.status == 200
    except (OSError, ValueError):
        raise Unavailable() from None


def service_port(config, role, target):
    ports = config["services"][role].get("ports", [])
    matches = [p for p in ports if integer(p.get("target")) == target
               and p.get("host_ip") == "127.0.0.1" and p.get("protocol", "tcp") == "tcp"]
    if len(matches) != 1:
        raise Unavailable()
    return integer(matches[0]["published"])


def runtime_projection(container, role, config):
    """Allowlisted fields only; arbitrary strings in inspect are never returned."""
    state = container.get("State", {})
    host = container.get("HostConfig", {})
    configured = config["services"][role]
    current_state = state.get("Status")
    health = state.get("Health", {}).get("Status", "not-configured")
    current_image = container.get("Config", {}).get("Image")
    runtime_ports = container.get("NetworkSettings", {}).get("Ports", {})
    host_ports = host.get("PortBindings", {})
    actual_ports = {(key, item.get("HostIp"), str(item.get("HostPort")))
                    for key, items in runtime_ports.items() for item in (items or [])}
    expected_ports = {(str(p["target"]) + "/" + p.get("protocol", "tcp"),
                       p.get("host_ip"), str(p["published"]))
                      for p in configured.get("ports", [])}
    expected_mounts = {(v["target"], v["type"], not v.get("read_only", False),
                       v.get("source") if v["type"] == "bind" else None)
                      for v in configured.get("volumes", [])}
    actual_mounts = {(v["Destination"], v["Type"], v["RW"],
                     v.get("Source") if v["Type"] == "bind" else None)
                    for v in container.get("Mounts", [])}
    logging = host.get("LogConfig", {})
    log_options = logging.get("Config", {})
    return {
        "state": current_state if current_state in STATES else "unknown",
        "health": health if health in HEALTH else "unknown",
        "restart_count": integer(container.get("RestartCount", 0)),
        "oom_killed": state.get("OOMKilled") is True,
        "loopback_bindings": loopback(runtime_ports) and loopback(host_ports)
                             and host.get("NetworkMode") != "host",
        "published_ports_match": actual_ports == expected_ports,
        "nnp": any(s in ("no-new-privileges", "no-new-privileges:true")
                   for s in host.get("SecurityOpt", [])),
        "privileged": host.get("Privileged") is True,
        "pid_exception_matches": host.get("PidMode", "") == ("host" if role == "node-exporter" else ""),
        "mounts_match": actual_mounts == expected_mounts,
        "readonly_matches": host.get("ReadonlyRootfs") is bool(configured.get("read_only", False)),
        "image_pin_matches": pin(current_image) and current_image == configured.get("image"),
        "logging_rotates": logging.get("Type") == "json-file"
                          and log_options.get("max-size") == "10m" and log_options.get("max-file") == "3",
        "resource_limits_present": host.get("Memory", 0) > 0 and host.get("NanoCpus", 0) > 0
                                   and (host.get("PidsLimit") or 0) > 0,
    }


def target_projection(targets, expected):
    active = targets.get("data", {}).get("activeTargets", [])
    summary = {}
    known_jobs = ("prometheus", "node-exporter", "cadvisor")
    for job in expected:
        selected = [t for t in active if t.get("labels", {}).get("job") == job]
        summary[job] = {
            "count": len(selected),
            "up": len(selected) == 1 and selected[0].get("health") == "up",
            "fresh": len(selected) == 1 and fresh_scrape(selected[0]),
            "scrape_error_present": any(bool(t.get("lastError")) for t in selected),
        }
    # Includes extra known jobs and unknown jobs; names/endpoints are suppressed.
    extra = sum(t.get("labels", {}).get("job") not in expected for t in active)
    return {"jobs": summary, "extra_target_count": extra,
            "dropped_target_count": len(targets.get("data", {}).get("droppedTargets", [])),
            "api_success": targets.get("status") == "success",
            "known_job_names_only": all(j in known_jobs for j in expected)}


def metric_values(response):
    if response.get("status") != "success" or response.get("data", {}).get("resultType") != "vector":
        raise Unavailable()
    rows = response["data"].get("result", [])
    if not rows:
        raise Unavailable()
    return [number(row["value"][1], maximum=100000) for row in rows]


class Review:
    def __init__(self, mode="lite", profiles=()):
        self.mode = mode
        self.profiles = tuple(profiles)
        self.checks = []
        self.compose = ["docker", "compose", "--env-file", ".env", "-f", "compose.yaml",
                        "-f", f"compose.{mode}.yaml"]
        for profile in profiles:
            self.compose += ["--profile", profile]

    def add(self, check, status, **facts):
        assert status in STATUSES
        self.checks.append({"check": check, "status": status, "facts": facts})

    def attempt(self, check, fn):
        try:
            fn()
        except (Unavailable, KeyError, TypeError, ValueError, IndexError, AttributeError, StopIteration):
            self.add(check, "NOT_VERIFIED")

    def collect(self):
        self.add("kuma_monitor_history", "REVIEW_REQUIRED")
        self.add("private_log_analysis", "REVIEW_REQUIRED")
        self.add("ssh_firewall_host_access", "REVIEW_REQUIRED")
        self.add("effective_users_capabilities", "REVIEW_REQUIRED")
        self.add("restart_resource_comparison", "REVIEW_REQUIRED")
        self.add("host_identity_storage_headroom", "REVIEW_REQUIRED")
        if not shutil.which("docker"):
            self.add("docker_cli", "NOT_VERIFIED")
            return self.report()
        try:
            context = os.environ.get("DOCKER_CONTEXT")
            endpoint = (command(["docker", "context", "inspect", context, "--format",
                                 "{{.Endpoints.docker.Host}}"])
                        if context else os.environ.get("DOCKER_HOST") or command(
                            ["docker", "context", "inspect", "--format", "{{.Endpoints.docker.Host}}"])).strip()
            if not endpoint.startswith("unix://"):
                self.add("local_unix_daemon", "FAIL")
                return self.report()
            info = json.loads(command(["docker", "info", "--format", "{{json .}}"]))
            self.add("local_unix_daemon", "PASS")
            if not (DEPLOY / ".env").is_file():
                self.add("local_environment", "NOT_VERIFIED")
                return self.report()
            self.add("environment_permissions",
                     "PASS" if stat.S_IMODE((DEPLOY / ".env").stat().st_mode) & 0o077 == 0 else "FAIL")
            config = json.loads(command(self.compose + ["config", "--format", "json"]))
            self.add("compose_render", "PASS")
            # Include stale disabled-profile services and project orphans, too.
            ids = command(["docker", "ps", "--all", "--quiet", "--filter",
                           "label=com.docker.compose.project=" + config["name"]]).split()
            inspected = json.loads(command(["docker", "inspect", *ids])) if ids else []
        except (Unavailable, ValueError):
            self.add("docker_compose_observation", "NOT_VERIFIED")
            return self.report()
        expected = CORE + tuple(r for r, p in OPTIONAL.items() if p in self.profiles)
        by_role = {}
        unknown = 0
        for container in inspected:
            role = container.get("Config", {}).get("Labels", {}).get("com.docker.compose.service")
            if role not in KNOWN:
                unknown += 1
            else:
                by_role.setdefault(role, []).append(container)
        self.add("unknown_project_services", "PASS" if unknown == 0 else "FAIL", count=unknown)
        for role, items in by_role.items():
            if role not in expected:
                running = sum(i.get("State", {}).get("Running") is True for i in items)
                self.add(role + ".disabled_profile", "FAIL" if running else "PASS", running_count=running)
        for role in expected:
            items = by_role.get(role, [])
            if len(items) != 1:
                self.add(role + ".presence", "FAIL", count=len(items))
                continue
            container = items[0]
            self.attempt(role + ".runtime", lambda r=role, c=container: self.runtime(r, c, config))
            cid = container["Id"]
            self.attempt(role + ".resources", lambda r=role, i=cid: self.resources(r, i))
            self.attempt(role + ".log_window", lambda r=role, i=cid: self.logs(r, i))
        self.attempt("disk_capacity", lambda: self.disk(info, by_role))
        self.attempt("host_listeners", self.listeners)
        self.attempt("prometheus_targets", lambda: self.prometheus(config))
        self.attempt("grafana_datasource", lambda: self.grafana(config))
        self.attempt("kuma_http", lambda: self.add(
            "kuma_http", "PASS" if http(service_port(config, "uptime-kuma", 3001), "/", as_json=False) else "FAIL"))
        return self.report()

    def runtime(self, role, container, config):
        facts = runtime_projection(container, role, config)
        self.add(role + ".state", "PASS" if facts["state"] == "running" else "FAIL",
                 state=facts["state"], restart_count=facts["restart_count"], oom_killed=facts["oom_killed"])
        expected_health = role in ("uptime-kuma", "prometheus", "grafana")
        status = ("PASS" if facts["health"] == "healthy" else "FAIL") if expected_health else "REVIEW_REQUIRED"
        self.add(role + ".docker_health", status, health=facts["health"])
        controls = ("loopback_bindings", "published_ports_match", "nnp", "pid_exception_matches",
                    "mounts_match", "readonly_matches", "image_pin_matches", "logging_rotates",
                    "resource_limits_present")
        for key in controls:
            self.add(role + "." + key, "PASS" if facts[key] else "FAIL")
        self.add(role + ".privilege_exception",
                 "REVIEW_REQUIRED" if role == "cadvisor" and facts["privileged"]
                 else "FAIL" if facts["privileged"] else "PASS")
        if facts["oom_killed"]:
            self.add(role + ".oom", "FAIL")

    def resources(self, role, cid):
        rows = command(["docker", "stats", "--no-stream", "--format", "{{json .}}", cid],
                       timeout=30).splitlines()
        if len(rows) != 1:
            raise Unavailable()
        row = json.loads(rows[0])
        cpu = row.get("CPUPerc", "")
        memory = row.get("MemPerc", "")
        if not re.fullmatch(r"\d+(\.\d+)?%", cpu) or not re.fullmatch(r"\d+(\.\d+)?%", memory):
            raise Unavailable()
        self.add(role + ".resources", "REVIEW_REQUIRED", cpu_percent=number(cpu[:-1], maximum=100000),
                 memory_limit_percent=number(memory[:-1], maximum=100))

    def logs(self, role, cid):
        raw = command(["docker", "logs", "--since", "30m", "--tail", "200", cid], log_stderr=True)
        lines = raw.splitlines()
        matches = sum(bool(re.search(r"\b(error|fatal|panic|exception)\b", line, re.I)) for line in lines)
        self.add(role + ".log_window", "REVIEW_REQUIRED", lines_observed=len(lines),
                 error_keyword_lines=matches, tail_limit=200, window_minutes=30)

    def disk(self, info, by_role):
        locations = {"docker_data": info["DockerRootDir"]}
        volumes = by_role.get("prometheus", [])
        if len(volumes) == 1:
            locations["prometheus_storage"] = next(m["Source"] for m in volumes[0].get("Mounts", [])
                                                    if m["Destination"] == "/prometheus")
        for label, path in locations.items():
            try:
                usage = shutil.disk_usage(path)
            except OSError:
                self.add(label + ".capacity", "NOT_VERIFIED")
                continue
            free = number(usage.free / usage.total * 100, maximum=100)
            self.add(label + ".capacity", "REVIEW_REQUIRED", free_percent=free,
                     free_gib=number(usage.free / 1024 ** 3))
        if "prometheus_storage" not in locations:
            self.add("prometheus_storage.capacity", "NOT_VERIFIED")

    def listeners(self):
        raw = command(["ss", "-H", "-lntu"])
        nonloopback = 0
        docker_api = 0
        for line in raw.splitlines():
            fields = line.split()
            if len(fields) < 6:
                raise Unavailable()
            address, port = fields[4].rsplit(":", 1)
            nonloopback += address.strip("[]") not in ("127.0.0.1", "::1")
            docker_api += port in ("2375", "2376")
        self.add("host_listeners", "REVIEW_REQUIRED", nonloopback_listener_count=nonloopback)
        self.add("docker_api_tcp_listener", "FAIL" if docker_api else "PASS",
                 standard_port_listener_count=docker_api)

    def prometheus(self, config):
        port = service_port(config, "prometheus", 9090)
        expected = ("prometheus", "node-exporter") + (("cadvisor",) if "containers" in self.profiles else ())
        facts = target_projection(http(port, "/api/v1/targets"), expected)
        good = facts["api_success"] and facts["extra_target_count"] == 0 and all(
            x["count"] == 1 and x["up"] and x["fresh"] and not x["scrape_error_present"]
            for x in facts["jobs"].values())
        self.add("prometheus_targets", "PASS" if good else "FAIL", **facts)
        queries = {
            "node_exporter_up": 'up{job="node-exporter"}',
            "host_cpu_5m_percent": '100 * (1 - avg(rate(node_cpu_seconds_total{job="node-exporter",mode="idle"}[5m])))',
            "host_memory_percent": '100 * (1 - node_memory_MemAvailable_bytes{job="node-exporter"} / node_memory_MemTotal_bytes{job="node-exporter"})',
            "filesystem_available_percent": '100 * node_filesystem_avail_bytes{job="node-exporter",fstype!~"tmpfs|overlay|squashfs"} / node_filesystem_size_bytes{job="node-exporter",fstype!~"tmpfs|overlay|squashfs"}',
        }
        for label, expression in queries.items():
            def check(label=label, expression=expression):
                values = metric_values(http(port, "/api/v1/query?" + urllib.parse.urlencode({"query": expression})))
                status = ("PASS" if values == [1.0] else "FAIL") if label == "node_exporter_up" else "REVIEW_REQUIRED"
                self.add(label, status, samples=len(values), minimum=min(values), maximum=max(values))
            self.attempt(label, check)

    def grafana(self, config):
        port = service_port(config, "grafana", 3000)
        health = http(port, "/api/health")
        self.add("grafana_http_health", "PASS" if health.get("database") == "ok" else "FAIL")
        env = config["services"]["grafana"]["environment"]
        user = env.get("GF_SECURITY_ADMIN_USER")
        secret = env.get("GF_SECURITY_ADMIN_PASSWORD")
        if not user or not secret or re.search(r"<[^>]+>", secret):
            raise Unavailable()
        credentials = (user, secret)
        data = http(port, "/api/datasources/uid/prometheus", credentials=credentials)
        good = (data.get("uid") == "prometheus" and data.get("type") == "prometheus"
                and data.get("url") == "http://prometheus:9090" and data.get("access") == "proxy")
        self.add("grafana_datasource_config", "PASS" if good else "FAIL")
        status = http(port, "/api/datasources/uid/prometheus/health", credentials=credentials)
        self.add("grafana_datasource_health", "PASS" if str(status.get("status", "")).upper() == "OK" else "FAIL")

    def report(self):
        try:
            revision = command(["git", "rev-parse", "HEAD"]).strip()
        except Unavailable:
            revision = "unknown"
        if not re.fullmatch(r"[0-9a-f]{40}", revision):
            revision = "unknown"
        return {"schema_version": 1, "exercise": "001-baseline-health-review",
                "status": "IN_PROGRESS", "publication_review": "PENDING",
                "homelab_identity": "REQUIRES_OPERATOR_CONFIRMATION",
                "collected_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                "repository_revision": revision,
                "collector_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                "mode": self.mode, "profiles": list(self.profiles), "checks": self.checks}


def write_report(report, output):
    content = json.dumps(report, indent=2, allow_nan=False) + "\n"
    if output is None:
        print(content, end="")
        return
    destination = Path(output).expanduser().resolve()
    if destination.is_relative_to(ROOT):
        raise Unavailable()
    try:
        fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o600)
        with os.fdopen(fd, "w") as stream:
            stream.write(content)
    except OSError:
        raise Unavailable() from None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--mode", choices=("lite", "full"), default="lite")
    parser.add_argument("--profile", choices=tuple(OPTIONAL.values()), action="append", default=[])
    parser.add_argument("--output", help="New report outside the checkout; omitted means sanitized stdout.")
    args = parser.parse_args()
    if args.profile and args.mode != "full":
        parser.error("optional profiles require full mode")
    try:
        # Check the output boundary before touching the daemon.
        if args.output and Path(args.output).expanduser().resolve().is_relative_to(ROOT):
            raise Unavailable()
        report = Review(args.mode, sorted(set(args.profile))).collect()
        write_report(report, args.output)
    except Exception:
        # Privacy boundary: even unexpected failures must not emit a traceback
        # containing private command/API values. Tests expose bugs using fixtures.
        print("Collection/output unavailable; no raw error details published.", file=sys.stderr)
        return 2
    states = {row["status"] for row in report["checks"]}
    return 1 if "FAIL" in states else 2 if states - {"PASS"} else 0


if __name__ == "__main__":
    sys.exit(main())
