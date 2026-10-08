"""Synthetic fixtures test privacy/failure behavior, not homelab operation."""
import contextlib
from datetime import datetime, timezone, timedelta
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import subprocess
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("health", ROOT / "deploy/scripts/baseline-health-review.py")
health = importlib.util.module_from_spec(spec)
spec.loader.exec_module(health)


def config():
    return {"name": "fixture-project", "services": {
        role: {"image": "example/component:1.2.3", "read_only": role == "node-exporter",
               "ports": [] if role == "node-exporter" else [
                   {"target": {"uptime-kuma": 3001, "prometheus": 9090, "grafana": 3000}[role],
                    "published": str({"uptime-kuma": 3001, "prometheus": 9090, "grafana": 3000}[role]),
                    "host_ip": "127.0.0.1"}],
               "volumes": []} for role in health.CORE}}


def container(role="grafana"):
    cfg = config()["services"][role]
    bindings = {str(p["target"]) + "/tcp": [{"HostIp": "127.0.0.1", "HostPort": p["published"]}]
                for p in cfg["ports"]}
    return {"Id": "FIXTURE_CONTAINER_ID", "RestartCount": 4,
            "Config": {"Image": "example/component:1.2.3", "User": "IDENTITY_SENTINEL",
                       "Env": ["TOKEN_SENTINEL"], "Labels": {"com.docker.compose.service": role}},
            "State": {"Status": "running", "Running": True, "OOMKilled": False,
                      "Health": {"Status": "healthy", "Log": [{"Output": "RAW_HEALTH_SENTINEL"}]}},
            "HostConfig": {"PortBindings": bindings, "NetworkMode": "fixture_network",
                           "SecurityOpt": ["no-new-privileges:true"], "Privileged": False,
                           "PidMode": "host" if role == "node-exporter" else "",
                           "ReadonlyRootfs": role == "node-exporter",
                           "Memory": 128 * 1024 ** 2, "NanoCpus": 250000000, "PidsLimit": 128,
                           "LogConfig": {"Type": "json-file", "Config": {"max-size": "10m", "max-file": "3"}}},
            "NetworkSettings": {"Ports": bindings}, "Mounts": []}


class PrivacyAndCorrectness(unittest.TestCase):
    def test_projection_has_no_arbitrary_runtime_strings(self):
        facts = health.runtime_projection(container(), "grafana", config())
        output = json.dumps(facts)
        for sentinel in ("IDENTITY_SENTINEL", "TOKEN_SENTINEL", "RAW_HEALTH_SENTINEL", "FIXTURE_CONTAINER_ID"):
            self.assertNotIn(sentinel, output)
        self.assertTrue(facts["published_ports_match"])
        self.assertTrue(facts["nnp"])
        self.assertEqual(facts["restart_count"], 4)

    def test_unknown_state_and_health_cannot_escape(self):
        c = container()
        c["State"].update({"Status": "IDENTITY_SENTINEL", "Health": {"Status": "TOKEN_SENTINEL"}})
        facts = health.runtime_projection(c, "grafana", config())
        self.assertEqual(facts["state"], "unknown")
        self.assertEqual(facts["health"], "unknown")

    def test_wildcard_ipv4_ipv6_and_host_network_are_rejected(self):
        for address in ("", "0" + ".0.0.0", "::"):
            c = container()
            c["NetworkSettings"]["Ports"]["3000/tcp"][0]["HostIp"] = address
            facts = health.runtime_projection(c, "grafana", config())
            self.assertFalse(facts["loopback_bindings"])
            self.assertFalse(facts["published_ports_match"])
        c = container()
        c["HostConfig"]["NetworkMode"] = "host"
        self.assertFalse(health.runtime_projection(c, "grafana", config())["loopback_bindings"])

    def test_extra_ports_mounts_and_missing_rotation_fail(self):
        c = container()
        c["NetworkSettings"]["Ports"]["4321/tcp"] = [{"HostIp": "127.0.0.1", "HostPort": "4321"}]
        c["Mounts"].append({"Source": "/FIXTURE_PRIVATE_PATH", "Destination": "/extra", "Type": "bind", "RW": True})
        c["HostConfig"]["LogConfig"]["Config"] = {}
        facts = health.runtime_projection(c, "grafana", config())
        self.assertFalse(facts["published_ports_match"])
        self.assertFalse(facts["mounts_match"])
        self.assertFalse(facts["logging_rotates"])

    def test_image_tags_and_digest_are_explicit(self):
        for image in ("example/component:latest", "example/component:1", "example/component"):
            self.assertFalse(health.pin(image))
        self.assertTrue(health.pin("example/component:v1.2.3-slim"))
        self.assertTrue(health.pin("example/component@sha256:" + "a" * 64))

    def test_secret_scrape_labels_and_errors_are_not_exported(self):
        target = {"labels": {"job": "node-exporter", "instance": "IDENTITY_SENTINEL"},
                  "health": "down", "lastError": "TOKEN_SENTINEL", "scrapeUrl": "PRIVATE_URL_SENTINEL",
                  "lastScrape": datetime.now(timezone.utc).isoformat()}
        facts = health.target_projection({"status": "success", "data": {"activeTargets": [target]}},
                                         ("node-exporter",))
        output = json.dumps(facts)
        for sentinel in ("IDENTITY_SENTINEL", "TOKEN_SENTINEL", "PRIVATE_URL_SENTINEL"):
            self.assertNotIn(sentinel, output)
        self.assertFalse(facts["jobs"]["node-exporter"]["up"])
        self.assertTrue(facts["jobs"]["node-exporter"]["scrape_error_present"])

    def test_missing_duplicate_extra_and_stale_targets_are_visible(self):
        target = {"labels": {"job": "node-exporter"}, "health": "up", "lastError": "",
                  "lastScrape": (datetime.now(timezone.utc) - timedelta(minutes=10)).isoformat()}
        facts = health.target_projection({"status": "success", "data": {"activeTargets": [
            target, target, {"labels": {"job": "IDENTITY_SENTINEL"}}]}}, ("prometheus", "node-exporter"))
        self.assertEqual(facts["jobs"]["prometheus"]["count"], 0)
        self.assertFalse(facts["jobs"]["node-exporter"]["up"])
        self.assertFalse(facts["jobs"]["node-exporter"]["fresh"])
        self.assertEqual(facts["extra_target_count"], 1)
        self.assertNotIn("IDENTITY_SENTINEL", json.dumps(facts))

    def test_nan_infinity_empty_or_malicious_metrics_never_pass(self):
        for value in ("NaN", "+Inf", "-Inf", "TOKEN_SENTINEL"):
            with self.assertRaises(health.Unavailable):
                health.metric_values({"status": "success", "data": {"resultType": "vector",
                    "result": [{"metric": {"instance": "IDENTITY_SENTINEL"}, "value": [0, value]}]}})
        with self.assertRaises(health.Unavailable):
            health.metric_values({"status": "success", "data": {"resultType": "vector", "result": []}})

    def test_bounded_log_window_exports_counts_only(self):
        review = health.Review()
        with patch.object(health, "command", return_value="IDENTITY_SENTINEL error TOKEN_SENTINEL\nnormal\n"):
            review.logs("grafana", "fixture")
        output = json.dumps(review.checks)
        self.assertNotIn("SENTINEL", output)
        self.assertEqual(review.checks[0]["facts"]["error_keyword_lines"], 1)
        self.assertEqual(review.checks[0]["status"], "REVIEW_REQUIRED")

    def test_raw_command_error_and_timeout_are_suppressed(self):
        result = subprocess.CompletedProcess([], 1, "TOKEN_SENTINEL", "IDENTITY_SENTINEL")
        with patch.object(health.subprocess, "run", return_value=result):
            with self.assertRaises(health.Unavailable) as caught:
                health.command(["docker", "info"])
        self.assertEqual(str(caught.exception), "")
        with patch.object(health.subprocess, "run", side_effect=subprocess.TimeoutExpired("TOKEN_SENTINEL", 1)):
            with self.assertRaises(health.Unavailable):
                health.command(["docker", "info"])

    def test_missing_docker_keeps_not_verified_and_manual_checks(self):
        with patch.object(health.shutil, "which", return_value=None):
            report = health.Review().collect()
        self.assertEqual(report["status"], "IN_PROGRESS")
        self.assertEqual(report["publication_review"], "PENDING")
        self.assertTrue(any(c["status"] == "NOT_VERIFIED" for c in report["checks"]))
        self.assertTrue(any(c["status"] == "REVIEW_REQUIRED" for c in report["checks"]))

    def test_remote_context_overrides_local_docker_host_and_is_refused(self):
        with patch.dict(os.environ, {"DOCKER_CONTEXT": "fixture-remote", "DOCKER_HOST": "unix:///fixture.sock"}):
            with patch.object(health.shutil, "which", return_value="/fixture/docker"):
                with patch.object(health, "command", return_value="tcp://REMOTE_SENTINEL:2376") as call:
                    report = health.Review().collect()
        self.assertTrue(any(c["check"] == "local_unix_daemon" and c["status"] == "FAIL" for c in report["checks"]))
        self.assertIn("fixture-remote", call.call_args_list[0].args[0])
        self.assertNotIn("REMOTE_SENTINEL", json.dumps(report))

    def test_in_repository_output_refused_and_external_output_private_no_overwrite(self):
        with self.assertRaises(health.Unavailable):
            health.write_report({}, health.ROOT / "private-evidence" / "fixture.json")
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "fixture.json"
            health.write_report({"safe": True}, output)
            self.assertEqual(stat.S_IMODE(output.stat().st_mode), 0o600)
            with self.assertRaises(health.Unavailable):
                health.write_report({"safe": False}, output)
            self.assertEqual(json.loads(output.read_text()), {"safe": True})

    def test_missing_volume_is_an_unverified_check_not_traceback(self):
        review = health.Review()
        review.attempt("disk_capacity", lambda: review.disk({"DockerRootDir": "/fixture/unavailable"},
                       {"prometheus": [{"Mounts": []}]}))
        self.assertEqual(review.checks[-1]["status"], "NOT_VERIFIED")

    def test_http_destination_and_redirect_policy(self):
        with self.assertRaises(health.Unavailable):
            health.http(70000, "/")
        self.assertIsNone(health.NoRedirect().redirect_request(None, None, None, None, None,
                                                               "http://PRIVATE_URL_SENTINEL/"))

    def test_cli_output_failure_does_not_print_private_path(self):
        output = io.StringIO()
        with patch.object(health.sys, "argv", ["collector", "--output", str(health.ROOT / "fixture.json")]):
            with contextlib.redirect_stderr(output):
                self.assertEqual(health.main(), 2)
        self.assertNotIn(str(health.ROOT), output.getvalue())

    def test_unexpected_failure_has_no_sensitive_traceback(self):
        output = io.StringIO()
        with patch.object(health.sys, "argv", ["collector"]):
            with patch.object(health.Review, "collect", side_effect=RuntimeError("TOKEN_SENTINEL")):
                with contextlib.redirect_stderr(output):
                    self.assertEqual(health.main(), 2)
        self.assertNotIn("TOKEN_SENTINEL", output.getvalue())
        self.assertNotIn("Traceback", output.getvalue())


if __name__ == "__main__":
    unittest.main()
