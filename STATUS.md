# Status — icml26-linear-recurrent-memory

**Paper:** *Why Linear Recurrent Memory Works in Partially Observable Reinforcement Learning*
**Authors:** Yike Zhao, Onno Eberhard, Malek Khammassi, Ali H. Sayed, and Michael Muehlebach
**Sources:** [arXiv:2605.31261](https://arxiv.org/abs/2605.31261) · [OpenReview ywjHJIkUgW](https://openreview.net/forum?id=ywjHJIkUgW)

## Release state

The cumulative evidence release is documented and repeatable. Claims 1, 2, 3,
and 5 have verified finite or proof-audit paths. Claim 4 is explicitly
`BLOCKED`; no proxy result is promoted as a RingWorld reproduction.

## Evidence summary

- C1 exact deterministic-transition logit identity: maximum discrepancy `0.0`;
  stochastic-transition control mismatch `14.814854322993483`.
- C2 theorem certificate: `xi=0.7206014018371381`, 416 bounded models
  searched, 312 satisfying the declared assumptions, no counterexample, and
  independent quadrature agreement.
- C3 action-controlled certificate: four actions, `xi=0.026480946096894026`,
  `kappa=554.2122392876782`, exact arbitrary-initialization error below
  `5.7e-14`, and independent action checks.
- C5 finite Section 6.1 sweep: 23 inverse-epsilon points, 20,000 trajectories
  per replicate, four replicates, all six decoders, Bayes LOF, uncertainty,
  and a rejected label-swap control.
- C4 RingWorld: blocked because the full protocol is not uniquely specified or
  runnable from the released sources. The blocker dossier calculates 56
  training runs, `1.68e9` environment steps, and at least `5.04e10`
  sample-epoch passes for the paper-faithful Figure 3 protocol.

## Evidence boundaries

- The C2/C3 `VERIFIED` labels come from executable audits of the paper's
  finite-state derivation and assumptions, not a proof-assistant formalization.
- The C5 experiment is finite empirical evidence and does not independently
  prove the universal C2/C3 limits.
- The C4 result is `BLOCKED`, not `FALSIFIED`; missing code and protocol detail
  prevent a fair faithful test.
- The arXiv HTML fingerprint and source audit are provenance records; no claim
  is made that the paper's plotted RingWorld curves were regenerated.

## Provenance

The complete claim ledger is in [`CLAIM_EVIDENCE.md`](CLAIM_EVIDENCE.md), source
and artifact details are in [`SOURCE_MANIFEST.md`](SOURCE_MANIFEST.md), and
branch/history state is in [`BRANCH_AUDIT.md`](BRANCH_AUDIT.md).
