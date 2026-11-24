# Subject-Level Split Integrity Audit

## Audit status

Verified against the restored manifests and the QC audit file.

## Split summary

| Split | Photo pairs | Unique subjects |
|---|---:|---:|
| Train | 6,133 | 2,018 |
| TestA | 1,684 | 87 |
| TestB | 1,158 | 400 |

Total photo pairs: 8,975

Sum of split-wise subject memberships: 2,505

Globally unique subject IDs: 2,504

## Pairwise subject overlap

| Comparison | Overlapping subjects |
|---|---:|
| Train vs TestA | 0 |
| Train vs TestB | 0 |
| TestA vs TestB | 1 |

The overlapping subject ID is:

`TlIG_3sXZLuH7T9nQMivDNnzJn4fFYQy1P0KqC3ldUQ`

This subject has 22 photo pairs in TestA and 6 eligible photo pairs in TestB.

## Interpretation and limitation

The original source metadata assigns the same subject ID to both TestA and TestB.
The official split membership has been preserved.

Train has no subject-ID overlap with either test split. However, TestA and TestB
are not fully independent at the subject-ID level.

The reason for the repeated source subject ID has not been established.
It must not be described as a confirmed identity match or confirmed source error
without further evidence.

TestA and TestB results should be reported separately. Any pooled evaluation
must disclose this overlap. A separate sensitivity analysis may evaluate the
effect of excluding the overlapping TestB subject, without modifying the
primary official-split manifests.

## QC exclusion policy

Only photo pairs recorded in the QC audit are excluded from the eligible
paired-view manifests. Original source files and official split assignments
are preserved.

Unique QC-excluded photo pairs:
- Train: 1
- TestA: 0
- TestB: 2

## Manifest integrity

The restored manifests were read back and verified:
- Train: 6,133 photo pairs, 2,018 subjects
- TestA: 1,684 photo pairs, 87 subjects
- TestB: 1,158 photo pairs, 400 subjects
- Combined: 8,975 photo pairs

Audit generated: 2026-11-19 08:33 UTC
