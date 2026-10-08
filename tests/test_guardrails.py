"""Security regressions use modified in-memory source, not runtime deployments."""
import importlib.util
from pathlib import Path
import tempfile
import unittest
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("guard", ROOT / "deploy/scripts/static-guardrails.py")
guard = importlib.util.module_from_spec(spec)
spec.loader.exec_module(guard)


class GuardrailTests(unittest.TestCase):
    def setUp(self):
        self.base = yaml.safe_load((ROOT / "deploy/compose.yaml").read_text())
        self.full = yaml.safe_load((ROOT / "deploy/compose.full.yaml").read_text())
        self.lite = yaml.safe_load((ROOT / "deploy/compose.lite.yaml").read_text())
        self.env = dict(line.split("=", 1) for line in (ROOT / "deploy/.env.example").read_text().splitlines()
                        if line and not line.startswith("#") and "=" in line)

    def check(self):
        return guard.compose_issues(self.base, self.full, self.lite, self.env)

    def test_repository_security_configuration(self):
        self.assertEqual(self.check(), [])

    def test_privileged_optional_service_cannot_be_default(self):
        self.full["services"]["cadvisor"].pop("profiles")
        self.assertIn("profile guard: cadvisor", self.check())

    def test_unreviewed_privileged_core_service_fails(self):
        self.base["services"]["grafana"]["privileged"] = True
        self.assertIn("privileged exception guard: grafana", self.check())

    def test_long_syntax_port_cannot_hide_wildcard(self):
        self.base["services"]["grafana"]["ports"] = [{"target": 3000, "published": 3000}]
        self.assertIn("loopback source guard: grafana", self.check())

    def test_logging_and_nnp_removal_fail(self):
        self.base["services"]["grafana"]["security_opt"] = []
        self.base["services"]["prometheus"]["logging"] = {}
        self.assertIn("NNP guard: grafana", self.check())
        self.assertIn("log rotation guard: prometheus", self.check())

    def test_extra_host_mount_fails_even_readonly(self):
        self.base["services"]["grafana"]["volumes"].append("/FIXTURE_PRIVATE_PATH:/extra:ro")
        self.assertIn("unreviewed volume/mount: grafana", self.check())

    def test_broad_image_tag_fails(self):
        self.env["GRAFANA_IMAGE"] = "example/component:latest"
        self.assertIn("image pin guard: grafana", self.check())

    def test_network_resource_and_capability_changes_fail(self):
        self.base["networks"]["metrics"]["internal"] = False
        self.lite["services"]["grafana"]["cpus"] = "0"
        self.base["services"]["grafana"]["cap_add"] = ["SYS_ADMIN"]
        issues = self.check()
        self.assertIn("internal metrics network guard", issues)
        self.assertIn("resource limit guard: lite/grafana", issues)
        self.assertIn("unreviewed capabilities/devices: grafana", issues)

    def test_links_and_anchors_checked_offline(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "README.md").write_text("[valid](other.md#some-title)\n[missing](absent.md)\n[anchor](other.md#absent)\n")
            (root / "other.md").write_text("# Some title\n")
            issues = guard.markdown_link_issues(root)
            self.assertEqual(len(issues), 2)

    def test_all_current_local_links(self):
        self.assertEqual(guard.markdown_link_issues(ROOT), [])

    def test_operational_evidence_cannot_link_to_planned_case(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "exercises"
            folder.mkdir()
            (root / "README.md").write_text("# Lab\n\n## Operational evidence\n[case](exercises/case.md)\n")
            (folder / "case.md").write_text("# Case\n\n**Status: PLANNED**\n")
            self.assertEqual(len(guard.operational_link_issues(root)), 1)
            (folder / "case.md").write_text("# Case\n\n**Status: COMPLETED**\n")
            self.assertEqual(guard.operational_link_issues(root), [])

    def test_exercise_addresses_rejected_without_printing_value(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            folder = root / "exercises"
            folder.mkdir()
            sample = folder / "README.md"
            sample.write_text("loopback example 127.0.0.1\n")
            self.assertEqual(guard.evidence_address_issues(root), [])
            synthetic = ".".join(("198", "51", "100", "42"))
            sample.write_text(synthetic)
            issues = guard.evidence_address_issues(root)
            self.assertEqual(len(issues), 1)
            self.assertNotIn(synthetic, issues[0])


if __name__ == "__main__":
    unittest.main()
