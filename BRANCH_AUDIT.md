# Branch and history audit

## Required final state

| Item | Required state |
|---|---|
| Repository | `MachineLearning-Nerd/icml26-linear-recurrent-memory` |
| Default branch | `main` |
| Published branches | `main` plus the eight descriptive audit/release branches below |
| Retired/generated names | no `master` or `orx/*` refs |
| Commit author and committer | `MachineLearning-Nerd <MachineLearning-Nerd@users.noreply.github.com>` |
| Co-author trailers | none |

## Branch map

| Final branch | Former branch | Role |
|---|---|---|
| `main` | `master` | cumulative final release |
| `baseline/validated-reproduction` | `orx/validated-baseline-judged-reproduction` | initial judged C1/C2 baseline and status |
| `experiment/claim-2-5-paper-sweep` | `orx/c2-c5-paper-faithful-20k-alf-sweep` | first paper-faithful ALF/C5 sweep |
| `experiment/claim-2-5-replicated-sweep` | `orx/c2-c5-replicated-alf-sweep` | four-seed replication and uncertainty |
| `audit/claim-3-action-controlled` | `orx/c3-action-controlled-exact-and-near-permutation` | exact action identity and near-permutation checks |
| `audit/claim-4-ringworld-blocker` | `orx/c4-faithful-ringworld-blocker-audit` | fail-closed C4 blocker dossier |
| `audit/claim-2-4-proof-source` | `orx/c2-c4-certified-analytic-and-source-forensic-aud` | theorem certificates and source/raster audit |
| `release/candidate-cumulative` | `orx/release-candidate-cumulative-evidence-and-logboo` | protected cumulative release candidate |
| `release/cumulative-proof-certificates` | `orx/promote-c2-c3-proof-certificates-into-cumulative` | final proof-certificate promotion; same tip as `main` |

No evidence branch is deleted. Branch names are descriptive so a reader can
understand the experiment or release stage without knowing the `orx` workflow.

## Verification

```bash
python verify_final.py
```

The verifier checks the target URL, current branch, absence of legacy refs,
canonical identities, co-author trailers, required artifacts, claim verdicts,
paper fingerprints, clean worktree, and 18 focused tests. The GitHub API check
performed during publication additionally verifies the exact published branch
list, default branch, repository metadata, tip, and remote commit identities.
