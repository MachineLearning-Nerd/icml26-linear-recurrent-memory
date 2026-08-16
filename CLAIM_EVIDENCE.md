# Claim-to-evidence audit

This ledger records what each paper claim means, which code produces it, what
independent check is applied, and where the final result is stored.

## Claim 1 — deterministic HMM log-belief identity

**Paper result:** Theorem 4.4 constructs a linear recurrent memory that
reproduces optimal pre-softmax belief logits for deterministic transitions.

**Production path:**

1. `repro/src/run_lrm.py:gen_hmm` creates an eight-state, twelve-observation
   column-stochastic permutation HMM.
2. `log_forward` computes the general log-sum-exp Bayesian forward recursion.
3. `linear_filter` computes `l_t = T l_{t-1} + log e_t`.
4. `max_abs_diff` compares the two independent paths over 40 observations.
5. A separately generated fully stochastic transition is used as a negative
   control.

**Stored result:** `outputs/lrm_summary.json` and the C1 tests record exact
agreement (`0.0`) and a control mismatch of `14.814854322993483`.

**Boundary:** The numerical instance has no transient states. The structural
deterministic/permutation route and arbitrary-initialization correction are
audited separately under C3; this is not a proof-assistant formalization.

## Claim 2 — time-invariant ALF under nearly deterministic transitions

**Paper result:** Theorem 5.7 gives a vanishing long-term decoding-error rate
under the paper's near-deterministic assumptions and the schedule
`delta_epsilon = lambda / log(1/epsilon)`.

**Production paths:**

- `repro/src/alf_two_state.py:run_claim2_5_evidence` runs the exact Section 6.1
  two-state finite sweep, scalar/full-vector recurrence cross-check, Bayes LOF
  comparator, and negative control.
- `repro/src/certified_audit.py:fixed_filter_certificate` enumerates every
  ordered recurrent-state pair, evaluates the Appendix-D log-MGF integral,
  constructs `xi`, `lambda`, `alpha`, and `kappa`, and checks the limiting
  schedule conditions.
- `independent_xi_checker` compares adaptive quadrature with an independent
  200001-point trapezoid calculation.
- `bounded_counterexample_search` checks all declared two- and three-state
  candidates in its bounded search; assumption-breaking controls must fail.

**Stored result:** `.openresearch/artifacts/claim_2/` contains the theorem
certificate, finite sweep, independent checker, negative control, runtime,
contract, method, limitations, and final `VERIFIED` evaluation.

**Boundary:** The finite sweep alone is not universal theorem evidence. The
committed `VERIFIED` status is the promoted proof-audit route, whose derivation
is described in [`repro/proof_derivations/claim_2.md`](repro/proof_derivations/claim_2.md).
The numeric constants are for the declared finite model, and the certificate is
not formalized in a proof assistant.

## Claim 3 — action-controlled filters

**Paper results:** Corollary 4.5 covers exact action-dependent permutation
transitions; Theorem 5.9 extends the near-deterministic guarantee to
action-controlled HMMs.

**Production paths:**

- `repro/src/action_controlled.py:action_model` defines four action-dependent
  permutation transitions and positive, separated emissions.
- `exact_action_identity` compares general action-conditioned log-sum-exp and
  linear paths over arbitrary initializations and action sequences.
- `independent_action_checker` uses a separately written index-based route.
- `simulate_near_action_model` runs the finite ALF/LOF sweep and controls.
- `repro/src/certified_audit.py:action_filter_certificate` takes the worst
  pairwise one-step exponent and proves the uniform finite-action certificate
  under nonanticipative action histories.

**Stored result:** `.openresearch/artifacts/claim_3/` records the exact
corollary checker, theorem certificate, independent quadrature, action sweep,
negative controls, and final `VERIFIED` evaluation.

The exact numerical route reaches maximum logit error
`5.684341886080802e-14`; the stochastic-action control mismatches by
`86.2514838846667`. The proof certificate reports
`xi=0.026480946096894026` and `kappa=554.2122392876782`.

**Boundary:** The action-uniform argument assumes finite state/action spaces,
positive distinct emissions, permutation backbones, and nonanticipative
actions. It is not a formal proof-assistant artifact.

## Claim 4 — RingWorld PPO experiment

**Paper result:** Section 6.2 compares direct ALF, direct LOF, Deep ALF, and S5
on the paper's RingWorld setting.

**Production path:** `repro/src/claim4_blocker.py:evaluate_claim4` checks the
paper source audit, protocol completeness, environment availability, resource
arithmetic, and whether any candidate implementation qualifies. It explicitly
rejects shortened runs, generic RNNs, adjacent S5 code, digitized plots, and
environment-only substitutes.

**Stored result:** `.openresearch/artifacts/claim_4/` contains the blocker
contract, source/code audit, independent resource arithmetic, rejected proxy,
runtime, and `BLOCKED` evaluation.

**Boundary:** This is not a failed scientific hypothesis test. It is a
reproducibility blocker caused by missing protocol/code/data and an unavailable
faithful training stack.

## Claim 5 — finite Section 6.1 sweep

**Paper result:** The valid schedules `sqrt(epsilon)` and
`0.7/log(1/epsilon)` improve as epsilon decreases, with the logarithmic schedule
beating the square-root schedule; invalid schedules do not converge.

**Production path:** `run_claim2_5_evidence` uses the paper's two-state
transition/emission matrices, 23 inverse-epsilon values in `[30,250]`, 20,000
trajectories per point and replicate, `k=1000`, four fixed replicate seeds,
three checkpoints, Wilson intervals, five ALF schedules, and Bayes-optimal LOF.
`verify_claim5` applies the predeclared endpoint, separation, and schedule-order
checks. The label-swap negative control intentionally corrupts the labels and
must be rejected.

**Stored result:** `.openresearch/artifacts/claim_5/` contains raw sweep data,
verifier output, independent recurrence output, negative control, runtime, and
the final `VERIFIED` evaluation.

**Boundary:** This is finite Monte Carlo evidence. It corroborates, but does
not replace, the proof-level route used for C2/C3.

## Release validation

`repro/src/release_checks.py:validate_release_candidate` protects the cumulative
`.trackio/logbook` pages and validates every claim contract, expected verdict,
required evidence file, theorem certificate, historical hash, and reachable
page. The focused suite in `repro/tests/test_lrm.py` exercises these checks and
the numerical/control routes; the release verifier reruns all 18 tests.
