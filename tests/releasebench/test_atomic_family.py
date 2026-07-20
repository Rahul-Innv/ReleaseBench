#!/usr/bin/env python3
"""ReleaseBench ten-skill atomic-family and fail-closed routing contracts."""

from __future__ import annotations

import hashlib
import importlib.util
import itertools
import json
import os
import re
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
FAMILY_PATH = ROOT / "skills" / "releasebench-atomic-family.json"
CASES_PATH = Path(__file__).with_name("atomic-routing-cases.json")
ROUTER_PATH = ROOT / "src" / "releasebench" / "router.py"
EXCLUDED_TREE_PARTS = {".git", "dist", "build", "releasebench.egg-info"}

EXPECTED_SKILLS = (
    "releasebench-route",
    "releasebench-prepare-repository",
    "releasebench-audit-repository",
    "releasebench-scan-secrets",
    "releasebench-scaffold-governance",
    "releasebench-showcase-readme",
    "releasebench-publish-repository",
    "releasebench-release-version",
    "releasebench-prepare-package",
    "releasebench-document-config",
)

DISPATCHABLE = EXPECTED_SKILLS[1:]

EXPECTED_EVAL_CASE_IDS = {
    "releasebench-route": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
        "trigger-nearmiss-2",
    ),
    "releasebench-prepare-repository": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
        "trigger-nearmiss-2",
    ),
    "releasebench-audit-repository": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
        "trigger-nearmiss-2",
        "trigger-nearmiss-sibling-orchestrator",
    ),
    "releasebench-scan-secrets": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
        "trigger-nearmiss-2",
        "trigger-nearmiss-sibling-review",
    ),
    "releasebench-scaffold-governance": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
        "trigger-nearmiss-2",
        "trigger-nearmiss-sibling-orchestrator",
    ),
    "releasebench-showcase-readme": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
    ),
    "releasebench-publish-repository": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
    ),
    "releasebench-release-version": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
    ),
    "releasebench-prepare-package": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
    ),
    "releasebench-document-config": (
        "trigger-positive-1",
        "trigger-positive-2",
        "trigger-positive-3",
        "trigger-nearmiss-1",
        "trigger-nearmiss-2",
    ),
}


def read_json(path: Path) -> dict:
    return json.loads(path.read_bytes().decode("utf-8"))


def sha256_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def product_text_paths() -> list[Path]:
    extensions = {".json", ".md", ".mjs", ".ps1", ".py", ".toml", ".yaml", ".yml"}
    roots = [
        ROOT / ".claude-plugin",
        ROOT / ".gitlab-ci.yml",
        ROOT / "docs",
        ROOT / "src",
        ROOT / "skills",
        ROOT / "AGENTS.md",
        ROOT / "CHANGELOG.md",
        ROOT / "README.md",
        ROOT / "ROADMAP.md",
        ROOT / "pyproject.toml",
    ]
    paths: list[Path] = []
    for item in roots:
        if item.is_file():
            paths.append(item)
        elif item.is_dir():
            paths.extend(path for path in item.rglob("*") if path.is_file() and path.suffix in extensions)
    return sorted(paths)


def privacy_text_paths() -> list[Path]:
    """Return product, CI, and tracked test text covered by the privacy gate."""

    extensions = {".json", ".md", ".mjs", ".ps1", ".py", ".toml", ".yaml", ".yml"}
    paths = set(product_text_paths())
    paths.update(
        path
        for path in (ROOT / "tests").rglob("*")
        if path.is_file() and path.suffix in extensions
    )
    return sorted(paths)


def load_router():
    spec = importlib.util.spec_from_file_location("releasebench_router_under_test", ROUTER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load router")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def request(request_id: str, **fields) -> dict:
    return {
        "contract_version": "releasebench.route-request/v1",
        "request_id": request_id,
        **fields,
    }


def parse_frontmatter(path: Path) -> dict[str, str]:
    text = path.read_bytes().decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    if not text.startswith("---\n"):
        raise AssertionError(f"missing frontmatter: {path}")
    block = text.split("\n---\n", 1)[0].splitlines()[1:]
    values: dict[str, str] = {}
    current: str | None = None
    for line in block:
        if line and not line.startswith(" ") and ":" in line:
            current, value = line.split(":", 1)
            values[current] = value.strip()
        elif current == "description":
            values[current] = f"{values[current]} {line.strip()}".strip()
    return values


class AtomicFamilyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.family = read_json(FAMILY_PATH)
        cls.cases = read_json(CASES_PATH)
        cls.router = load_router()

    def test_exact_ten_skill_ids_and_three_non_skill_primitives(self) -> None:
        leaves = self.family["leaves"]
        self.assertEqual(list(EXPECTED_SKILLS), [item["id"] for item in leaves])
        self.assertEqual(10, len(leaves))
        internals = self.family["internal_primitives"]
        self.assertEqual(
            {
                "releasebench-core-lesson-reader",
                "releasebench-core-plugin-manifest",
                "releasebench-core-portable-agent-guide",
            },
            {item["id"] for item in internals},
        )
        self.assertTrue(all(item["public_skill"] is False for item in internals))
        self.assertEqual(49, sum(item["eval_cases"] for item in leaves))

    def test_each_skill_has_one_outcome_and_four_non_goals(self) -> None:
        for leaf in self.family["leaves"]:
            self.assertTrue(leaf["intent_owner"])
            self.assertTrue(leaf["independently_measurable_outcome"])
            self.assertEqual(4, len(leaf["non_goals"]))
            self.assertEqual(4, len(set(leaf["non_goals"])))
        router = self.family["router_contract"]
        self.assertFalse(router["contains_leaf_implementation"])
        self.assertEqual("fail-closed", router["ambiguity_policy"])
        self.assertEqual("src/releasebench/router.py", router["entrypoint"])

    def test_plugin_membership_is_exactly_the_ten_canonical_skill_directories(self) -> None:
        actual = sorted(
            path.name
            for path in (ROOT / "skills").iterdir()
            if path.is_dir() and (path / "SKILL.md").is_file()
        )
        self.assertEqual(sorted(EXPECTED_SKILLS), actual)
        plugin = read_json(ROOT / ".claude-plugin" / "plugin.json")
        self.assertEqual("releasebench", plugin["name"])
        self.assertEqual("0.1.1", plugin["version"])
        marketplace = read_json(ROOT / ".claude-plugin" / "marketplace.json")
        self.assertEqual(plugin["version"], marketplace["plugins"][0]["version"])
        self.assertIn('version = "0.1.1"', (ROOT / "pyproject.toml").read_text(encoding="utf-8"))
        self.assertIn(
            '__version__ = "0.1.1"',
            (ROOT / "src" / "releasebench" / "__init__.py").read_text(encoding="utf-8"),
        )
        self.assertEqual("Rahul Krishna", plugin["author"]["name"])
        self.assertIn("ten atomic skills", plugin["description"])

    def test_gitlab_ci_runs_only_offline_contracts(self) -> None:
        text = (ROOT / ".gitlab-ci.yml").read_text(encoding="utf-8")
        self.assertIn("python -B tests/releasebench/run_tests.py", text)
        self.assertIn("find skills -type f -name '*.mjs' -exec node --check '{}' \\;", text)
        self.assertNotIn("-exec node --check '{}' +", text)
        self.assertNotRegex(
            text,
            r"(?i)\b(?:curl|wget|git\s+(?:fetch|pull|push)|npm\s+publish|"
            r"twine\s+upload|cargo\s+publish)\b",
        )

        runner_path = Path(__file__).with_name("run_tests.py")
        spec = importlib.util.spec_from_file_location("releasebench_test_runner", runner_path)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        self.assertEqual((), runner.result_contract_violations(
            tests_run=runner.EXPECTED_TEST_COUNT, failures=0, errors=0, skipped=0
        ))
        for drift in (
            dict(tests_run=runner.EXPECTED_TEST_COUNT - 1, failures=0, errors=0, skipped=0),
            dict(tests_run=runner.EXPECTED_TEST_COUNT, failures=0, errors=0, skipped=1),
            dict(tests_run=runner.EXPECTED_TEST_COUNT, failures=1, errors=0, skipped=0),
            dict(tests_run=runner.EXPECTED_TEST_COUNT, failures=0, errors=1, skipped=0),
        ):
            with self.subTest(drift=drift):
                self.assertTrue(runner.result_contract_violations(**drift))

    def test_all_repository_json_documents_parse(self) -> None:
        paths = sorted(
            path
            for path in ROOT.rglob("*.json")
            if not (EXCLUDED_TREE_PARTS & set(path.parts))
        )
        self.assertTrue(paths)
        for path in paths:
            with self.subTest(path=path.relative_to(ROOT)):
                json.loads(path.read_text(encoding="utf-8"))

    def test_skill_metadata_uses_exact_canonical_ids_and_inactive_codex_policy(self) -> None:
        for skill_id in EXPECTED_SKILLS:
            folder = ROOT / "skills" / skill_id
            frontmatter = parse_frontmatter(folder / "SKILL.md")
            self.assertEqual(skill_id, frontmatter["name"])
            self.assertTrue(frontmatter["description"].strip())
            metadata = (folder / "agents" / "openai.yaml").read_text(encoding="utf-8")
            self.assertIn(f"${skill_id}", metadata)
            self.assertIn("allow_implicit_invocation: false", metadata)

    def test_exact_49_eval_cases_are_preserved_by_leaf_and_id(self) -> None:
        total = 0
        qualified_ids: set[str] = set()
        for skill_id, expected_ids in EXPECTED_EVAL_CASE_IDS.items():
            document = read_json(ROOT / "skills" / skill_id / "evals" / "evals.json")
            self.assertEqual(skill_id, document["skill_name"])
            cases = document["evals"]
            self.assertEqual(expected_ids, tuple(case["id"] for case in cases))
            self.assertTrue(any(case["should_trigger"] is True for case in cases))
            self.assertTrue(any(case["should_trigger"] is False for case in cases))
            for case in cases:
                self.assertEqual(
                    {"id", "prompt", "should_trigger"},
                    {key for key in case if key != "expected_behavior"},
                )
                self.assertIs(type(case["should_trigger"]), bool)
                self.assertTrue(case["prompt"].strip())
                qualified = f"{skill_id}/{case['id']}"
                self.assertNotIn(qualified, qualified_ids)
                qualified_ids.add(qualified)
            total += len(cases)
        self.assertEqual(49, total)
        self.assertEqual(49, len(qualified_ids))

    def test_portable_guide_is_canonical_and_byte_equal_at_both_surfaces(self) -> None:
        root_guide = (ROOT / "AGENTS.md").read_bytes()
        nested_guide = (ROOT / "skills" / "releasebench-route" / "AGENTS.md").read_bytes()
        self.assertEqual(root_guide, nested_guide)
        text = root_guide.decode("utf-8")
        for skill_id in EXPECTED_SKILLS:
            self.assertIn(skill_id, text)
        self.assertIn(
            "remains the lifecycle, eligibility, supersession, and routing-priority",
            text,
        )
        self.assertIn("producing lane never self-certifies", text)

    def test_product_surfaces_contain_no_owner_home_path_or_high_confidence_secret(self) -> None:
        forbidden_roots = {
            Path.home().as_posix().casefold(),
        }
        generic_home_path = re.compile(
            r"(?i)(?:[a-z]:)?[\\/](?:users|home)[\\/][^\\/:\s\"'<>]+"
        )
        secret_patterns = (
            re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
            re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
            re.compile(r"\bsk-[A-Za-z0-9]{20,}\b"),
            re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b"),
        )
        covered = privacy_text_paths()
        self.assertIn((ROOT / ".gitlab-ci.yml").resolve(), {path.resolve() for path in covered})
        self.assertIn(Path(__file__).resolve(), {path.resolve() for path in covered})
        for path in covered:
            text = path.read_text(encoding="utf-8")
            normalized = text.replace("\\", "/").casefold()
            for forbidden_root in forbidden_roots:
                self.assertNotIn(forbidden_root, normalized, path)
            self.assertIsNone(generic_home_path.search(text), path)
            for pattern in secret_patterns:
                self.assertIsNone(pattern.search(text), f"{pattern.pattern} in {path}")

    def test_trigger_and_near_miss_fixtures_cover_every_skill_once(self) -> None:
        positives = self.cases["positive_cases"]
        near_misses = self.cases["near_miss_cases"]
        self.assertEqual(set(EXPECTED_SKILLS), {item["trigger_skill"] for item in positives})
        self.assertEqual(set(EXPECTED_SKILLS), {item["excluded_skill"] for item in near_misses})
        for item in [*positives, *near_misses]:
            self.assertTrue(item["prompt"].strip())

    def test_every_positive_router_fixture_selects_one_expected_leaf(self) -> None:
        for item in self.cases["positive_cases"]:
            payload = request(item["id"], **item["request"])
            first = self.router.dispatch(payload)
            second = self.router.dispatch(payload)
            self.assertEqual(first, second)
            self.assertEqual("selected", first["decision"])
            self.assertEqual(item["expected_leaf"], first["leaf_id"])
            claimed = first["receipt_sha256"]
            without_hash = {key: value for key, value in first.items() if key != "receipt_sha256"}
            self.assertEqual(claimed, self.router.canonical_sha256(without_hash))

    def test_all_pairwise_direct_intent_collisions_fail_closed(self) -> None:
        intents = sorted(self.router.INTENT_TO_LEAF)
        observed = set()
        for left, right in itertools.combinations(intents, 2):
            result = self.router.dispatch(request(f"{left}-{right}", intents=[left, right]))
            self.assertEqual("no-safe-route", result["decision"])
            self.assertIsNone(result["leaf_id"])
            self.assertEqual("AMBIGUOUS_MULTIPLE_INTENTS", result["reason_code"])
            observed.add(frozenset((left, right)))
        self.assertEqual(36, len(observed))

    def test_explicit_leaf_only_wins_when_inferred_intent_agrees(self) -> None:
        for intent, leaf in self.router.INTENT_TO_LEAF.items():
            result = self.router.dispatch(
                request(f"explicit-{intent}", explicit_leaf=leaf, intents=[intent])
            )
            self.assertEqual("selected", result["decision"])
            self.assertEqual(leaf, result["leaf_id"])
        conflict = self.router.dispatch(
            request(
                "explicit-conflict",
                explicit_leaf="releasebench-audit-repository",
                intents=["scan-secrets"],
            )
        )
        self.assertEqual("no-safe-route", conflict["decision"])
        self.assertEqual("AMBIGUOUS_EXPLICIT_AND_INTENT", conflict["reason_code"])

    def test_full_flow_selects_only_the_first_incomplete_stage(self) -> None:
        completed: list[str] = []
        for expected in self.router.FULL_FLOW_ORDER:
            result = self.router.dispatch(
                request("flow-" + expected, full_flow=True, completed_leaves=completed)
            )
            self.assertEqual(expected, result["leaf_id"])
            self.assertEqual("FIRST_INCOMPLETE_FULL_FLOW_STAGE", result["reason_code"])
            completed.append(expected)
        done = self.router.dispatch(request("flow-done", full_flow=True, completed_leaves=completed))
        self.assertEqual("no-safe-route", done["decision"])
        self.assertEqual("FULL_FLOW_LOCAL_STAGES_COMPLETE", done["reason_code"])

    def test_every_receipt_keeps_all_eight_outward_modes_closed(self) -> None:
        for intent in self.router.INTENT_TO_LEAF:
            result = self.router.dispatch(request(intent, intents=[intent]))
            self.assertFalse(result["outward_actions_authorized"])
            self.assertFalse(result["outward_actions_executed"])
            self.assertEqual(list(self.router.CLOSED_ACTIONS), result["closed_actions"])
            self.assertEqual("candidate-inactive", result["authority_state"])
            self.assertEqual("private-prepublic", result["visibility_state"])

    def test_cli_is_byte_equal_to_in_process_dispatch(self) -> None:
        payload = request("cli", intents=["audit-repository"])
        expected = self.router.canonical_bytes(self.router.dispatch(payload)) + b"\n"
        completed = subprocess.run(
            [sys.executable, "-B", str(ROUTER_PATH), "-"],
            input=self.router.canonical_bytes(payload) + b"\n",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            cwd=ROOT,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1", "PYTHONHASHSEED": "0"},
            check=False,
        )
        self.assertEqual(0, completed.returncode, completed.stderr.decode("utf-8"))
        self.assertEqual(expected, completed.stdout)
        self.assertEqual(b"", completed.stderr)

    def test_malformed_requests_raise_stable_fail_closed_codes(self) -> None:
        invalid = (
            ({}, "CONTRACT_VERSION_MISMATCH"),
            (request("extra", surprise=True), "UNDECLARED_FIELD"),
            (request("unknown", intents=["invented"]), "UNKNOWN_INTENT"),
            (request("recursive", explicit_leaf="releasebench-route"), "UNKNOWN_OR_RECURSIVE_LEAF"),
            (request("duplicate", intents=["scan-secrets", "scan-secrets"]), "DUPLICATE_INTENT"),
            (
                request(
                    "state-conflict",
                    completed_leaves=["releasebench-showcase-readme"],
                    not_applicable_leaves=["releasebench-showcase-readme"],
                ),
                "CONFLICTING_LEAF_STATE",
            ),
        )
        for payload, code in invalid:
            with self.subTest(code=code):
                with self.assertRaises(self.router.ContractError) as raised:
                    self.router.dispatch(payload)
                self.assertEqual(code, raised.exception.code)

    def test_support_surfaces_are_retained_under_canonical_owners(self) -> None:
        self.assertTrue((ROOT / "skills" / "releasebench-audit-repository" / "scripts" / "audit-repo.mjs").is_file())
        self.assertTrue((ROOT / "skills" / "releasebench-scan-secrets" / "scripts" / "scan-secrets.mjs").is_file())
        self.assertEqual(6, len(list((ROOT / "skills" / "releasebench-scaffold-governance" / "templates").iterdir())))
        self.assertEqual(3, len(list((ROOT / "skills" / "releasebench-document-config" / "templates").iterdir())))
        self.assertEqual(2, len(list((ROOT / "skills" / "releasebench-showcase-readme" / "assets").iterdir())))
        lesson_hashes = {
            hashlib.sha256((ROOT / "skills" / skill_id / "scripts" / "read-lessons.mjs").read_bytes()).hexdigest()
            for skill_id in EXPECTED_SKILLS
        }
        self.assertEqual(
            {"1456e9a6afbb5f0832b2ccae48280d9f5e46271013898d0fc914a47b77bd68fb"},
            lesson_hashes,
        )

    def test_readme_collapses_exact_receipts_without_changing_the_examples(self) -> None:
        readme_lines = (ROOT / "README.md").read_text(encoding="utf-8").splitlines()
        in_details = False
        long_lines: list[str] = []
        for line in readme_lines:
            if line == "<details>":
                self.assertFalse(in_details)
                in_details = True
            elif line == "</details>":
                self.assertTrue(in_details)
                in_details = False
            if len(line) > 400:
                self.assertTrue(in_details, "long README output must be collapsed by default")
                long_lines.append(line)

        self.assertFalse(in_details)
        self.assertEqual(2, readme_lines.count("<summary>Exact one-line receipt</summary>"))
        self.assertEqual(2, len(long_lines))
        self.assertTrue(all('"receipt_sha256"' in line for line in long_lines))
        expected_result = "tests=22 failures=0 errors=0 skipped=0"
        self.assertIn(expected_result, "\n".join(readme_lines))
        self.assertIn(expected_result, (ROOT / "STATUS.md").read_text(encoding="utf-8"))
        self.assertNotIn("19 checks", "\n".join(readme_lines))

    def test_python_package_metadata_links_to_public_project(self) -> None:
        metadata = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
        for expected in (
            'Repository = "https://gitlab.com/krahul02004/ReleaseBench"',
            'Issues = "https://gitlab.com/krahul02004/ReleaseBench/-/work_items"',
            'Changelog = "https://gitlab.com/krahul02004/ReleaseBench/-/blob/main/CHANGELOG.md"',
        ):
            self.assertIn(expected, metadata)

    def test_published_changelog_entry_does_not_claim_missing_git_provenance(self) -> None:
        changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")
        compact = " ".join(changelog.split())
        self.assertIn("## [Unreleased]\n\n## [0.1.1] - 2026-07-19", changelog)
        self.assertIn("## [0.1.0] - 2026-07-18", changelog)
        self.assertIn("There is no matching Git tag or\nGitLab Release", changelog)
        self.assertNotIn("compare/v0.1.0", changelog)
        self.assertNotIn("## [0.1.0] - candidate", changelog)
        self.assertNotIn(
            "without creating a local tag, host Release, or public artifact",
            compact,
        )
        release_surfaces = "\n".join(
            (ROOT / relative).read_text(encoding="utf-8")
            for relative in (
                "ROADMAP.md",
                "docs/public/OWNER-HANDOFF.md",
                "docs/public/READINESS.md",
                "docs/public/RELEASE-CANDIDATE.md",
            )
        )
        compact_release_surfaces = " ".join(release_surfaces.split())
        for stale in (
            "git tag -a v0.1.0",
            "git push origin v0.1.0",
            "first unshipped `0.1.0` candidate",
            "ReleaseBench has no shipped version",
            "existing `v0.1.0` tag",
            "GitHub-path-specific",
        ):
            self.assertNotIn(stale, release_surfaces)
        self.assertIn("PATCH version 0.1.1 is selected", release_surfaces)
        self.assertIn(
            "Never create a retroactive `v0.1.0` tag or Release",
            compact_release_surfaces,
        )

    def test_router_has_no_network_or_process_execution_surface(self) -> None:
        source = ROUTER_PATH.read_text(encoding="utf-8")
        for forbidden in ("subprocess", "socket", "urllib", "requests", "http.client", "os.system"):
            self.assertNotIn(forbidden, source)


if __name__ == "__main__":
    unittest.main()
