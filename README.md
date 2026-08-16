# icml26-linear-recurrent-memory

Independent evidence audit for **Why Linear Recurrent Memory Works in Partially
Observable Reinforcement Learning** (ICML 2026).

## Paper

- **Authors:** Yike Zhao, Onno Eberhard, Malek Khammassi, Ali H. Sayed, and Michael Muehlebach
- **Paper:** [arXiv:2605.31261](https://arxiv.org/abs/2605.31261)
- **OpenReview:** [ywjHJIkUgW](https://openreview.net/forum?id=ywjHJIkUgW)
- **Canonical audit repository:** <https://github.com/MachineLearning-Nerd/icml26-linear-recurrent-memory>
- **Collection:** ICML 2026 reproduction audit collection

The paper studies why linear recurrent memories can work in partially
observable reinforcement learning. It constructs filters that reproduce HMM
belief logits exactly under deterministic transitions, gives asymptotic error
guarantees for nearly deterministic transitions, extends the construction to
action-controlled HMMs, and illustrates the ideas with finite simulations and a
RingWorld learning experiment.

This repository is an independent audit. The paper and the author publication
record did not provide a direct RingWorld implementation, so the release keeps
that result blocked instead of substituting an adjacent S5 repository or a
digitized plot.

## Claim status

| Paper claim | Status | What the evidence actually establishes |
|---|---|---|
| Claim 1 — deterministic-transition log-belief reproduction (Theorem 4.4) | `VERIFIED_FINITE` | General log-sum-exp forward recursion and the linear recurrence agree at maximum absolute error `0.0` on the declared permutation HMM; a fully stochastic transition produces a `14.814854322993483` mismatch. |
| Claim 2 — time-invariant ALF under nearly deterministic transitions (Theorem 5.7) | `VERIFIED_PROOF_AUDIT` | The executable Appendix-D certificate has `xi=0.7206014018371381`, finite `lambda`, `alpha`, and `kappa`, passes independent dense quadrature, and finds no counterexample in 416 bounded candidates (312 assumption-satisfying). The finite sweep is corroboration, not the universal proof by itself. |
| Claim 3 — action-controlled exact and near-permutation filters (Corollary 4.5 and Theorem 5.9) | `VERIFIED_PROOF_AUDIT` | Four action permutations pass the exact arbitrary-initialization identity and the uniform exponent certificate (`xi=0.026480946096894026`, `kappa=554.2122392876782`); independent quadrature and action controls pass. |
| Claim 4 — RingWorld PPO comparison (Section 6.2) | `BLOCKED` | The paper source lacks enough protocol detail and raw curves, no direct implementation is available, the required stack is absent, and the faithful protocol would require 56 trainings and at least `1.68e9` environment steps. |
| Claim 5 — two-state Section 6.1 ALF sweep | `VERIFIED_FINITE` | The exact 23-point, 20,000-trajectory-per-replicate, `k=1000` sweep covers both valid and all three invalid schedules, Bayes LOF, Wilson intervals, independent recurrences, and a label-swap negative control. |

The proof-audit labels mean that the repository contains an executable audit of
the stated finite-state derivation and its assumptions; they are not a
proof-assistant formalization. Claim 4 remains blocked in the final release.

## How each claim is produced

| Claim | Producer path | Independent check | Stored evidence |
|---|---|---|---|
| C1 | `repro/src/run_lrm.py:log_forward`, `linear_filter`, `max_abs_diff` | General SciPy log-sum-exp path versus the linear recurrence; stochastic-transition negative control | `outputs/lrm_summary.json` and `repro/tests/test_lrm.py` |
| C2 | `alf_two_state.run_claim2_5_evidence` for the finite sweep; `certified_audit.fixed_filter_certificate` for the proof route | Scalar/full-vector recurrences, exact LOF, adaptive quadrature versus 200001-point trapezoid, bounded assumption search, failed identical-emission/non-permutation controls | `.openresearch/artifacts/claim_2/` |
| C3 | `action_controlled.exact_action_identity`, `simulate_near_action_model`, and `certified_audit.action_filter_certificate` | Independent action-index checker, uniform pair-separation certificate, dense quadrature, wrong-action/stochastic-action controls | `.openresearch/artifacts/claim_3/` |
| C4 | `claim4_blocker.evaluate_claim4`, `resource_contract`, `reject_proxy_as_full_evidence` | Protocol-completeness, source-availability, resource arithmetic, and proxy rejection checks | `.openresearch/artifacts/claim_4/` |
| C5 | `alf_two_state.run_claim2_5_evidence` and `verify_claim5` | Exact 23-point contract, schedule separations, uncertainty, full-vector recurrence, label-swap negative control | `.openresearch/artifacts/claim_5/` |

`repro/src/run_lrm.py` orchestrates the complete cumulative audit. It first
writes the basic C1 summary, then runs the C2/C5 finite sweep, the C3 action
checks, the C4 blocker, and finally `certified_audit.py`, which promotes the
proof-level C2/C3 evidence into the cumulative release artifacts. Running only
the finite sweep is therefore intentionally weaker than the committed final
claim status.

## Branches

The original repository used `master` plus eight `orx/*` branches. They are
retained under descriptive names and their roles are recorded in
[`BRANCH_AUDIT.md`](BRANCH_AUDIT.md):

- `main` — cumulative release and current paper audit.
- `baseline/validated-reproduction` — initial judged reproduction.
- `experiment/claim-2-5-paper-sweep` — paper-faithful 20,000-trajectory ALF sweep.
- `experiment/claim-2-5-replicated-sweep` — four-seed replication of that sweep.
- `audit/claim-3-action-controlled` — action-controlled exact and near-permutation checks.
- `audit/claim-4-ringworld-blocker` — fail-closed RingWorld blocker dossier.
- `audit/claim-2-4-proof-source` — theorem certificates and source/raster audit.
- `release/candidate-cumulative` — protected cumulative release candidate.
- `release/cumulative-proof-certificates` — promoted proof certificates, identical to the final `main` tip.

## Repository map

- [`repro/src/`](repro/src/) — producers, independent checkers, proof
  certificates, and the Claim 4 blocker.
- [`repro/tests/test_lrm.py`](repro/tests/test_lrm.py) — 18 focused tests.
- [`.openresearch/artifacts/`](.openresearch/artifacts/) — claim contracts,
  methods, raw finite sweeps, verifier outputs, limitations, and runtime data.
- [`.trackio/logbook/`](.trackio/logbook/) — protected rendered campaign
  logbook; `repro/src/release_checks.py` verifies its historical hashes and
  claim verdicts.
- [`repro/proof_derivations/`](repro/proof_derivations/) — human-readable
  derivations for the C2 and C3 proof routes.
- [`outputs/lrm_summary.json`](outputs/lrm_summary.json) — compact C1/C2
  illustration summary, not the complete cumulative evidence ledger.

## Reproduce and verify

Python 3.12 is required by the pinned environment.

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt

# Focused release checks (18 tests; quick).
python -m pytest -q

# Full cumulative producer; writes the claim artifacts and can be CPU-intensive.
python repro/src/run_lrm.py

# Fail-closed release gate.
python verify_final.py
```

The verifier checks the committed claim boundaries, protected logbook, source
fingerprints, clean refs, canonical attribution, and focused tests. It does not
claim that a finite Monte Carlo run proves a universal asymptotic statement.

## Citation and thanks

```bibtex
@article{zhao2026linear,
  title         = {Why Linear Recurrent Memory Works in Partially Observable Reinforcement Learning},
  author        = {Zhao, Yike and Eberhard, Onno and Khammassi, Malek and Sayed, Ali H. and Muehlebach, Michael},
  journal       = {arXiv preprint arXiv:2605.31261},
  year          = {2026},
  doi           = {10.48550/arXiv.2605.31261},
  url           = {https://arxiv.org/abs/2605.31261}
}
```

Thank you to Yike Zhao, Onno Eberhard, Malek Khammassi, Ali H. Sayed, and
Michael Muehlebach for developing a clear theoretical account of linear memory
in partially observable reinforcement learning. The paper's explicit claims
and assumptions made it possible to build independent numerical and
proof-audit paths, while the absence of a faithful RingWorld implementation
also made the limits of reproducibility clear. This repository is independent
and is not author-endorsed.

All publication commits are attributed to
`MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>`.
