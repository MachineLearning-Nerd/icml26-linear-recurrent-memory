#!/usr/bin/env python3
"""Fail-closed release verifier for the linear-memory evidence audit."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
FINAL_REMOTE = "https://github.com/MachineLearning-Nerd/icml26-linear-recurrent-memory"
CANONICAL_NAME = "MachineLearning-Nerd"
CANONICAL_EMAIL = "MachineLearning-Nerd@users.noreply.github.com"
PAPER_ID = "2605.31261"
PAPER_SHA256 = "e6ed4e6be5e80ab9f65eac02be852add36872fc660fa780cfcf1e68ac0f94250"
FINAL_BRANCHES = {
    "main",
    "baseline/validated-reproduction",
    "experiment/claim-2-5-paper-sweep",
    "experiment/claim-2-5-replicated-sweep",
    "audit/claim-3-action-controlled",
    "audit/claim-4-ringworld-blocker",
    "audit/claim-2-4-proof-source",
    "release/candidate-cumulative",
    "release/cumulative-proof-certificates",
}


def fail(message: str) -> None:
    raise SystemExit(f"VERIFY_FAIL: {message}")


def run(*args: str) -> str:
    result = subprocess.run(args, cwd=ROOT, text=True, capture_output=True, check=False)
    if result.returncode:
        fail(f"command failed: {' '.join(args)}\n{result.stdout}{result.stderr}")
    return result.stdout.strip()


def require_files() -> None:
    required = [
        "README.md",
        "STATUS.md",
        "CLAIM_EVIDENCE.md",
        "SOURCE_MANIFEST.md",
        "BRANCH_AUDIT.md",
        "CITATION.cff",
        "requirements.txt",
        "verify_final.py",
        "repro/src/run_lrm.py",
        "repro/src/alf_two_state.py",
        "repro/src/action_controlled.py",
        "repro/src/certified_audit.py",
        "repro/src/claim4_blocker.py",
        "repro/src/release_checks.py",
        "repro/tests/test_lrm.py",
        "repro/proof_derivations/claim_2.md",
        "repro/proof_derivations/claim_3.md",
        "outputs/lrm_summary.json",
        ".trackio/logbook/logbook.json",
        ".trackio/logbook/release/SHA256SUMS.txt",
    ]
    for claim in range(1, 6):
        directory = ROOT / ".openresearch" / "artifacts" / f"claim_{claim}"
        required.extend(
            str(Path(".openresearch") / "artifacts" / f"claim_{claim}" / name)
            for name in (
                "EVAL.md",
                "claim_contract.json",
                "limitations.md",
                "method.md",
                "runtime.json",
                "source_audit.md",
                "verifier_output.json",
                "independent_checker_output.json",
                "negative_control_output.json",
            )
        )
        if claim in (2, 3):
            required.extend(
                str(Path(".openresearch") / "artifacts" / f"claim_{claim}" / name)
                for name in ("proof_derivation.md", "theorem_certificate.json")
            )
        if claim == 4:
            required.append(str(directory.relative_to(ROOT) / "public_code_audit.json"))
        if claim == 5:
            required.append(str(directory.relative_to(ROOT) / "raw_two_state_sweep.csv"))
        if claim == 3:
            required.append(str(directory.relative_to(ROOT) / "raw_action_sweep.csv"))
    missing = [path for path in required if not (ROOT / path).is_file()]
    if missing:
        fail(f"missing required files: {', '.join(missing)}")


def check_docs() -> None:
    readme = (ROOT / "README.md").read_text()
    status = (ROOT / "STATUS.md").read_text()
    evidence = (ROOT / "CLAIM_EVIDENCE.md").read_text()
    manifest = (ROOT / "SOURCE_MANIFEST.md").read_text()
    branch_audit = (ROOT / "BRANCH_AUDIT.md").read_text()
    citation = (ROOT / "CITATION.cff").read_text()
    for marker in (
        "Why Linear Recurrent Memory Works",
        "Yike Zhao",
        "Michael Muehlebach",
        "2605.31261",
        "VERIFIED_PROOF_AUDIT",
        "BLOCKED",
        "Thank you",
        "MachineLearning-Nerd",
    ):
        if marker not in readme:
            fail(f"README is missing marker: {marker}")
    for marker in (
        "Claim 1",
        "Claim 2",
        "Claim 3",
        "Claim 4",
        "Claim 5",
        "run_claim2_5_evidence",
        "fixed_filter_certificate",
        "action_filter_certificate",
        "claim4_blocker.py",
        "not a proof-assistant",
    ):
        if marker not in evidence:
            fail(f"claim evidence is missing marker: {marker}")
    for marker in (PAPER_SHA256, "2605.31261", ".openresearch/artifacts", "s5rl"):
        if marker not in manifest:
            fail(f"source manifest is missing marker: {marker}")
    for marker in (
        "main",
        "master",
        "orx/*",
        "baseline/validated-reproduction",
        "release/cumulative-proof-certificates",
        "Co-author trailers",
    ):
        if marker not in branch_audit:
            fail(f"branch audit is missing marker: {marker}")
    for marker in ("repository-code:", "2605.31261", "Zhao", "Muehlebach"):
        if marker not in citation:
            fail(f"citation file is missing marker: {marker}")
    if "icml26-repro-ywjHJIkUgW" in readme or "icml26-repro-ywjHJIkUgW" in status:
        fail("legacy repository slug remains in release docs")
    if "31262" in (ROOT / "repro/src/run_lrm.py").read_text():
        fail("incorrect arXiv identifier remains in the producer")
    requirements = [line for line in (ROOT / "requirements.txt").read_text().splitlines() if line]
    if requirements != [
        "numpy==2.5.1",
        "scipy==1.18.0",
        "matplotlib==3.11.0",
        "pytest==9.1.1",
    ]:
        fail("requirements.txt changed from the audited environment")


def check_git_state() -> None:
    if sys.version_info < (3, 12):
        fail("Python 3.12 or newer is required by the pinned environment")
    if run("git", "branch", "--show-current") != "main":
        fail("current branch is not main")
    remote = run("git", "remote", "get-url", "origin").removesuffix(".git")
    if remote != FINAL_REMOTE:
        fail(f"origin is {remote!r}, expected {FINAL_REMOTE!r}")
    if run("git", "status", "--porcelain"):
        fail("working tree is not clean")
    refs = run("git", "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes").splitlines()
    if "refs/heads/main" not in refs:
        fail("refs/heads/main is missing")
    legacy = [
        ref
        for ref in refs
        if ref.endswith("/master") or "/orx/" in ref or "icml26-repro-ywjHJIkUgW" in ref
    ]
    if legacy:
        fail(f"legacy refs remain: {legacy}")
    remote_names = {
        ref.removeprefix("refs/remotes/origin/")
        for ref in refs
        if ref.startswith("refs/remotes/origin/") and ref != "refs/remotes/origin/HEAD"
    }
    if not FINAL_BRANCHES <= remote_names:
        fail(f"published branch refs are incomplete: {sorted(remote_names)}")
    records = run("git", "log", "--all", "--format=%H%x00%an%x00%ae%x00%cn%x00%ce").splitlines()
    if not records:
        fail("no reachable commits")
    expected = (CANONICAL_NAME, CANONICAL_EMAIL, CANONICAL_NAME, CANONICAL_EMAIL)
    for record in records:
        fields = record.split("\x00")
        if len(fields) != 5 or tuple(fields[1:]) != expected:
            fail(f"non-canonical commit identity: {record}")
    messages = run("git", "log", "--all", "--format=%B")
    if any(line.lower().startswith("co-authored-by:") for line in messages.splitlines()):
        fail("a reachable commit contains a co-author trailer")


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text())


def check_artifacts() -> None:
    summary = load_json("outputs/lrm_summary.json")
    if summary.get("paper") != "arXiv 2605.31261":
        fail(f"compact summary paper changed: {summary.get('paper')}")
    if summary.get("C1", {}).get("exact_match") is not True:
        fail(f"C1 exact result failed: {summary.get('C1')}")
    if summary.get("C1", {}).get("max_abs_diff", 1) >= 1e-10:
        fail(f"C1 threshold failed: {summary.get('C1')}")
    if summary.get("control", {}).get("stochastic_mismatch") is not True:
        fail(f"C1 negative control failed: {summary.get('control')}")
    c2_summary = summary.get("C2", {})
    if c2_summary.get("vanishes") is not True or c2_summary.get("final_tv", 1) >= 0.05:
        fail(f"compact C2 result failed: {c2_summary}")

    expected_verdicts = {1: "VERIFIED", 2: "VERIFIED", 3: "VERIFIED", 4: "BLOCKED", 5: "VERIFIED"}
    for claim, verdict in expected_verdicts.items():
        eval_text = (ROOT / ".openresearch" / "artifacts" / f"claim_{claim}" / "EVAL.md").read_text()
        if f"**{verdict}**" not in eval_text:
            fail(f"claim {claim} EVAL does not declare {verdict}")

    c2 = load_json(".openresearch/artifacts/claim_2/verifier_output.json")
    if c2.get("verdict") != "VERIFIED" or not c2.get("theorem_certificate_passed"):
        fail(f"C2 verifier failed: {c2}")
    c2_cert = load_json(".openresearch/artifacts/claim_2/theorem_certificate.json")
    if c2_cert.get("claim2_certificate_verdict") != "VERIFIED":
        fail(f"C2 theorem certificate failed: {c2_cert.get('claim2_certificate_verdict')}")
    if c2.get("bounded_models_searched") != 416 or c2.get("assumption_satisfying_models") != 312:
        fail(f"C2 bounded audit coverage changed: {c2}")
    if c2.get("counterexample_found") is not False:
        fail(f"C2 counterexample status changed: {c2}")

    c3 = load_json(".openresearch/artifacts/claim_3/verifier_output.json")
    if c3.get("verdict") != "VERIFIED" or not c3.get("theorem_5_9_uniform_certificate_passed"):
        fail(f"C3 verifier failed: {c3}")
    if c3.get("actions") != 4 or c3.get("all_actions_preserve_pair_separation") is not True:
        fail(f"C3 action coverage changed: {c3}")
    c3_exact = load_json(".openresearch/artifacts/claim_3/exact_corollary_checker_output.json")
    if not c3_exact.get("passed") or c3_exact.get("maximum_absolute_logit_error", 1) >= 1e-12:
        fail(f"C3 exact identity failed: {c3_exact}")

    c4 = load_json(".openresearch/artifacts/claim_4/verifier_output.json")
    if c4.get("claim4_verdict") != "BLOCKED":
        fail(f"C4 boundary changed: {c4}")
    blockers = c4.get("blockers", {})
    if not blockers or not all(blockers.values()):
        fail(f"C4 blocker dossier is incomplete: {c4}")
    if c4.get("resource_contract", {}).get("figure3_training_runs") != 56:
        fail(f"C4 resource contract changed: {c4.get('resource_contract')}")

    c5 = load_json(".openresearch/artifacts/claim_5/verifier_output.json")
    if c5.get("all_passed") is not True or c5.get("checks", {}).get("exact_23_point_grid") is not True:
        fail(f"C5 verifier failed: {c5}")
    c5_independent = load_json(".openresearch/artifacts/claim_5/independent_checker_output.json")
    if c5_independent.get("passed") is not True:
        fail(f"C5 independent checker failed: {c5_independent}")


def check_tests() -> None:
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "-q"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    output = f"{result.stdout}\n{result.stderr}"
    if result.returncode:
        fail(f"focused tests failed:\n{output}")
    if "18 passed" not in output:
        fail(f"focused test count changed:\n{output}")


def main() -> None:
    require_files()
    check_docs()
    check_git_state()
    check_artifacts()
    check_tests()
    print("FINAL_VERIFICATION_PASS")
    print(f"repository={FINAL_REMOTE}")
    print("branch=main")
    print(f"published_branch_refs={len(FINAL_BRANCHES)}")
    print(f"reachable_commits={len(run('git', 'rev-list', '--all').splitlines())}")
    print("commit_identity=canonical")
    print("claim_boundaries=PASS")
    print("focused_tests=PASS")


if __name__ == "__main__":
    main()
