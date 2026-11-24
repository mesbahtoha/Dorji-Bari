# P0 Remaining Limitations — Recommendations

**Date:** 2026-11-24  
**Scope:** recommendations for the P0.6 supervisor report; no new experiments, training, recalibration, or historical edits.

**Overall status:** **UNRESOLVED — DISCLOSE AS LIMITATION**

---

## A. E05-U Nested GroupKFold Provenance

**Recommendation:** Report the distinction explicitly:

- Outer 5-fold evidence is present (config, code, 25 fold-result rows, five outer_fold labels).
- Inner 4-fold evidence exists only in the config and point-OOF code; no inner-fold assignments are saved.
- The uncertainty cell uses 5 inner folds.
- Do not claim the full 5×4 nested design is independently proven.

**Supervisor-report language:**

> “The saved E05 artifacts support a five-outer-fold structure but do not contain inner-fold assignments or subject-level outer training membership. The configuration documents four inner folds, while the fully nested uncertainty code uses five. The full 5×4 nested procedure is therefore not independently verified from saved artifacts.”

**No action:** Do not fabricate fold assignments or rerun E05-U in this phase.

---

## B. Fixed-Alpha vs Tuned-Alpha Residual Mismatch

**Recommendation:** Document the exact cause and avoid treating the two residual sets as interchangeable:

- Saved point OOF: tuned alpha via GridSearchCV, 4 inner folds.
- Fully nested uncertainty: fixed `Ridge(alpha=1.0)`, 5 inner folds.
- 4,438/10,090 residual rows differ; maximum 2.645083 cm; mismatch concentrated in waist/hip.

**Supervisor-report language:**

> “The uncertainty audit’s actual base errors are not the saved nested-OOF residuals. The uncertainty pipeline regenerates residuals with a fixed alpha of 1.0, whereas the saved point OOF used per-fold tuned alpha. This is an implementation/configuration inconsistency, not an arithmetic error in the saved point metrics.”

**No action:** Do not replace predictions or residuals.

---

## C. Missing Uncertainty-Model Artifact

**Recommendation:** Limit claims to saved predictions/metrics. State that no E05-U fitted model binary exists in the reproduction root; only E01–E04 checkpoints are serialized. Do not claim model-level reproducibility.

**Supervisor-report language:**

> “E05-U model predictions and metrics were audited, but the fitted uncertainty model is not saved. The uncertainty model cannot be independently reloaded; only its saved outputs and code are available.”

**No action:** Do not train or generate a replacement model.

---

## D. Missing TestA/TestB Risk Scores

**Recommendation:** Restrict risk-ranking claims to Train OOF. State that TestA/TestB risk scores are absent and cannot be evaluated without producing new test-split scores, which is outside this audit and would require a supervisor-approved protocol.

**Supervisor-report language:**

> “Risk-ranking results are Train OOF only (n=2,018). No TestA/TestB uncertainty or risk scores are saved; test-split risk performance is not evaluated.”

**No action:** Do not use TestA/TestB for tuning or scoring in this phase.

---

## E. TestB Undercoverage

**Recommendation:** Report the measured gaps, not a causal claim:

- TestB 15/15 target × nominal combinations below nominal.
- Mean TestB coverage 0.81200 vs TestA 0.89885.
- TestB 80% coverage 0.6800–0.7300; 90% 0.8000–0.8525; 95% 0.8675–0.9225.

**Supervisor-report language:**

> “Train-OOF-calibrated intervals undercover on TestB at every target × nominal combination. This is consistent with distribution or calibration sensitivity; the cause is not established. TestB was not used for recalibration.”

**No action:** Do not recalibrate or tune on TestB.

---

## F. Shared TestA–TestB Source ID

**Recommendation:** Retain the official split and disclose the ID with conflicting attributes:

- `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`;
- TestA 22 pairs; TestB 6 official pairs;
- TestA height 163.2 cm; TestB 168.0 cm;
- target/measurement records differ; identity unverified.

**Supervisor-report language:**

> “A shared source subject ID appears in both TestA and TestB. Its identity is unverified and the records carry conflicting height and measurement values. The official split is retained; the ID was not removed.”

**No action:** Do not infer identity or alter splits.

---

## G. TestB Clean-Manifest Discrepancy

**Recommendation:** Keep the discrepancy visible and use the official manifests for analysis:

- `testB_clean_manifest.csv`: 1,159 rows;
- official/preprocessed TestB: 1,158 rows;
- extra pair: `578f12cd7dbbf39ccebc3116eaea41d6`, subject `TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`;
- pair is QC-excluded.

**Supervisor-report language:**

> “The clean TestB manifest contains one stale QC-excluded pair not present in the official or preprocessed TestB manifests. The historical files were not modified; all official counts use 1,158 TestB pairs.”

**No action:** Do not repair or overwrite the clean manifest.

---

## H. Historical Colab Environment

**Recommendation:** Cite only the archived evidence:

- Python 3.13.16, Linux, PyTorch 2.14.1+cu130, OpenCV 4.14.0, NumPy 2.4.6, pandas 2.2.3, scikit-learn 1.6.1, Tesla T4, CUDA 13.0.
- Current notebook metadata reflects local Python 3.14.6, not the historical kernel.
- Exact command, kernel spec, session log and complete warnings are unavailable.

**Supervisor-report language:**

> “The archived environment report documents the historical Colab stack and T4 GPU. The exact historical command and runtime session are not archived; exact Colab runtime equivalence is not claimed.”

**No action:** Do not invent a historical command or kernel.

---

## Overall Treatment in P0.6

1. Use **E01/E04 exact-reproduction** statements without qualification beyond the documented isolated-copy and runtime caveats.
2. Use **coverage/uncertainty/risk numerical results** as verified against saved artifacts.
3. Add a dedicated limitations subsection covering A, C, D, E, F and H.
4. Use B and G as documentation clarifications, not as repaired science.
5. Do not state that the dataset or uncertainty pipeline is fully validated.
6. Do not request supervisor approval on the user’s behalf; list the issues for G0 review.
7. If the supervisor requires full 5×4 nested provenance, propose a **future audited run** that saves fold assignments and model artifacts; do not reinterpret existing artifacts.

**Final status: UNRESOLVED — DISCLOSE AS LIMITATION.**

No historical artifact was modified in this phase.
