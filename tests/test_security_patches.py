"""Offline security patch regressions: no Docker daemon or live homelab needed."""
import copy
import importlib.util
from pathlib import Path
import re
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("homelab_guardrails_security", ROOT / "deploy/scripts/static-guardrails.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class SecurityPatchTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = yaml.safe_load((ROOT / "deploy/compose.yaml").read_text())
        cls.full = yaml.safe_load((ROOT / "deploy/compose.full.yaml").read_text())
        cls.lite = yaml.safe_load((ROOT / "deploy/compose.lite.yaml").read_text())
        cls.env = dict(
            line.split("=", 1) for line in (ROOT / "deploy/.env.example").read_text().splitlines()
            if line and not line.startswith("#") and "=" in line
        )

    def test_security_candidate_images_are_exact_pins(self):
        expected = {
            "UPTIME_KUMA_IMAGE": "louislam/uptime-kuma:2.5.6-slim",
            "PROMETHEUS_IMAGE": "prom/prometheus:v3.13.4",
            "NODE_EXPORTER_IMAGE": "prom/node-exporter:v1.12.1",
            "GRAFANA_IMAGE": "grafana/grafana:13.1.8",
            "CADVISOR_IMAGE": "ghcr.io/google/cadvisor:0.60.6",
            "ADGUARD_HOME_IMAGE": "adguard/adguardhome:v0.107.79",
            "CROWDSEC_IMAGE": "crowdsecurity/crowdsec:1.7.8-debian",
        }
        for name, image in expected.items():
            self.assertEqual(self.env[name], image)
            self.assertTrue(guard.image_pin(image), image)

    def test_current_compose_security_guards_pass(self):
        self.assertEqual(guard.compose_issues(self.base, self.full, self.lite, self.env), [])

    def test_prometheus_has_no_http_shutdown_or_remote_write_features(self):
        flags = self.base["services"]["prometheus"]["command"]
        self.assertFalse(any(flag.startswith("--web.enable-") for flag in flags))
        self.assertIn("--storage.tsdb.path=/prometheus", flags)
        self.assertIn("--config.file=/etc/prometheus/prometheus.yml", flags)

    def test_prometheus_lifecycle_reintroduction_is_blocked(self):
        for unsafe in (
            "--web.enable-lifecycle",
            "--web.enable-admin-api",
            "--web.enable-remote-write-receiver",
            "--web.enable-otlp-receiver",
            "--web.listen-address=0.0.0.0:9090",
        ):
            base = copy.deepcopy(self.base)
            base["services"]["prometheus"]["command"].append(unsafe)
            issues = guard.compose_issues(base, self.full, self.lite, self.env)
            self.assertIn("prometheus HTTP lifecycle/admin and command guard", issues)

    def test_updater_does_not_enable_optional_privileged_profiles(self):
        self.assertEqual(self.full["services"]["cadvisor"]["profiles"], ["containers"])
        self.assertTrue(self.full["services"]["cadvisor"]["privileged"])
        self.assertEqual(self.full["services"]["adguard-home"]["profiles"], ["dns"])
        self.assertEqual(self.full["services"]["crowdsec"]["profiles"], ["detection"])
        self.assertFalse(self.base["networks"]["metrics"]["internal"] is not True)

    def test_updated_actions_are_pinned_to_immutable_sha_and_minimum_permissions(self):
        workflow = (ROOT / ".github/workflows/repository-validation.yml").read_text()
        actions = re.findall(r"^\s*uses:\s*(actions/[\w-]+)@([^\s#]+)", workflow, re.M)
        self.assertEqual({x[0] for x in actions}, {"actions/checkout", "actions/upload-artifact"})
        self.assertTrue(all(re.fullmatch(r"[0-9a-f]{40}", sha) for _, sha in actions))
        self.assertIn("contents: read", workflow)
        self.assertIn("persist-credentials: false", workflow)
        self.assertIn("runs-on: ubuntu-24.04", workflow)
        self.assertNotIn("schedule:", workflow)

    def test_sensitive_configuration_stays_placeholder_only(self):
        text = (ROOT / "deploy/.env.example").read_text()
        self.assertEqual(self.env["GRAFANA_ADMIN_PASSWORD"], "<CHANGE_ME_LONG_RANDOM_PASSWORD>")
        self.assertNotIn("privileged: true", (ROOT / "deploy/compose.yaml").read_text())
        self.assertNotIn("GF_SECURITY_ADMIN_PASSWORD__FILE", (ROOT / "deploy/compose.yaml").read_text())
        self.assertIn("restore-test", (ROOT / "docs/version-matrix.md").read_text().lower())


if __name__ == "__main__":
    unittest.main()
