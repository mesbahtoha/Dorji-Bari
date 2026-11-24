# BodyM Research Field Mapping
## DorjiBari Dataset Audit

Audit date: 2026-11-19

## Dataset Sources

Dataset: Amazon BodyM
Official dataset documentation:
https://registry.opendata.aws/bodym/

Original research paper:
Human Body Measurement Estimation with Adversarial Augmentation

## Model Input

| CSV | Column | Meaning | Unit | Status |
|---|---|---|---|---|
| hwg_metadata.csv | height_cm | Subject stature | cm | Candidate input |

## Target Measurements

Source: measurements.csv

| Column | Meaning | Unit |
|---|---|---|
| chest | Chest girth | cm |
| waist | Waist girth | cm |
| hip | Hip girth | cm |
| shoulder-breadth | Shoulder breadth | cm |
| arm-length | Arm length | cm |

## Height Field Distinction

The BodyM paper describes subject height separately from
14 mesh-derived measurements.

The paper lists head-to-heel length among the 14
mesh-derived measurements.

The measurements.csv field named "height" is therefore
a candidate mapping to head-to-heel length. This mapping
requires source-schema confirmation.

The hwg_metadata.csv field "height_cm" is treated as
subject stature and is the candidate model input.

The two fields must not be treated as interchangeable.

## Research Restrictions

1. Do not overwrite original CSV files.
2. Do not silently replace one height field with another.
3. Do not use measurements.height as a model input.
4. Do not use TestA or TestB for model training or tuning.
5. Preserve subject-level separation.
6. Keep all five target measurements in centimetres.
7. Investigate unusual values before deciding whether
   any observation should be excluded.

## Current Status

Five target columns have no missing values in the
audited splits.

Height discrepancy investigation completed.

Exact source-schema mapping of measurements.height
remains to be confirmed.
