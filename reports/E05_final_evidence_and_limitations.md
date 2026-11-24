# E05 — Final Evidence Consolidation

## Scope

E05 evaluates uncertainty estimation and selective verification for five BodyM measurements using subject-level cross-validation and previously saved held-out predictions.

The analysis uses chest, waist, hip, shoulder breadth, and arm length.

## Core experimental evidence

### Fully nested uncertainty estimation

The fully nested cross-fitted comparison found that Extra Trees provided only a small overall improvement over the median absolute-error baseline. Its gains were concentrated in hip and, to a much smaller extent, waist. It did not improve all measurement targets.

### Held-out interval coverage

Intervals calibrated from Train OOF residuals showed generally closer-to-nominal coverage on TestA than on TestB. All 15 TestB target-by-nominal-level combinations were below nominal coverage in the observed evaluation. This indicates that the Train-derived thresholds did not transfer reliably to TestB.

### Selective verification

Risk ranking was more useful for hip and waist than for shoulder breadth and arm length. Chest showed intermediate evidence. These results are based on cross-fitted Train predictions and should not be described as independent TestA/TestB validation.

### Tolerance sensitivity

Illustrative thresholds were used only for sensitivity analysis. They are not clinical, regulatory, or industry-standard tailoring tolerances.

The strongest observed Top-20% result was hip at ±5 cm, where Ridge captured approximately 50.75% of out-of-tolerance events and the enrichment ratio was approximately 2.54. The corresponding bootstrap 95% CI for enrichment was approximately 2.27–2.83.

Waist at ±5 cm with Ridge and chest at ±5 cm with Extra Trees also showed enrichment above random selection.

## Limitations

1. The uncertainty meta-model results are based on cross-fitted Train predictions, not a separate external population.
2. The inner OOF base models and outer-fold base models use different training-set sizes. This train-size mismatch may affect the residual distribution used by the meta-model.
3. TestB interval undercoverage indicates calibration drift or distribution sensitivity. TestB must not be used to tune thresholds if it is retained as a held-out evaluation set.
4. TestA and TestB share one subject ID in the official source metadata. Train has no subject overlap with either split, but TestA and TestB are not fully subject-disjoint.
5. Bootstrap intervals resample fixed cross-fitted predictions. They do not include full model-training uncertainty.
6. Feature-error associations are exploratory correlations, not causal explanations or validated individual uncertainty estimates.
7. Selective verification identifies candidates for review. It does not demonstrate that human verification actually corrects the measurement or improves final garment fit.
8. The illustrative tolerance grid requires validation against a clearly specified tailoring protocol and real operational requirements.

## Claims that are currently supported

- Silhouette geometry combined with height substantially improved the evaluated Ridge baseline compared with height alone.
- Ridge was the strongest of the tested classical models under the selected Train-only grouped CV comparison.
- Train-derived prediction intervals undercovered on TestB.
- Cross-fitted risk ranking showed promising selective verification signals, strongest for hip and waist.
- Tolerance-based sensitivity analysis found enrichment above random selection for the tested illustrative thresholds.

## Claims that are not yet established

- Guaranteed measurement accuracy for new users.
- Clinical or industry-standard tolerance compliance.
- Guaranteed nominal prediction interval coverage.
- Demonstrated reduction in real-world tailoring errors.
- Causal explanations for TestB performance differences.
- Generalization to populations or capture conditions outside the evaluated BodyM data.

## Reproducibility note

All reported conclusions must remain linked to the saved predictions, metrics, configurations, and audit files. Any missing artifact identified by the inventory must be restored or explicitly documented before paper submission.

## Inventory status

- Expected artifacts checked: 21
- Missing artifacts: 0
- Read errors: 0

### Missing files

- None

### Read errors

- None

## Important interpretation

The selective-verification results are evidence of risk enrichment in this cross-fitted dataset. They are not yet evidence that a deployed human-in-the-loop system reduces real-world measurement error. That requires an operational verification protocol and evaluation of corrected or re-measured outcomes.