# KoboToolbox Scripts

This folder contains the two main scripts used in the KoboToolbox → SSSOM → JSON-LD workflow.

The current workflow is:

```text
1. Pull raw Kobo record
2. Use AI prompt / manual review to create or update the SSSOM TSV
3. Run the SSSOM transformer to generate JSON-LD
```

## Current Script Flow

| Step | Script / Action                    | Purpose                                                                                            | Main Output                               |
| ---- | ---------------------------------- | -------------------------------------------------------------------------------------------------- | ----------------------------------------- |
| 1    | `01_pull_kobo_raw_json_records.py` | Pulls one KoboToolbox record from the Gaia metadata authoring form using the record ID.            | `records/raw/record_<id>_raw.json`        |
| 2    | AI prompt / manual mapping review  | Creates or updates the SSSOM TSV crosswalk from Kobo JSON fields to Schema.org JSON-LD properties. | `sssom/<mapping_name>.sssom.tsv`          |
| 3    | `02_sssom_to_jsonld.py`            | Uses the SSSOM TSV and raw Kobo JSON to generate JSON-LD.                                          | `records/outputs/record_<id>_output.json` |

## Script 1: Pull raw Kobo JSON

Use this script to fetch a specific Kobo record.

Example for record 216:

```bash
python authoring/kobotoolbox/scripts/01_pull_kobo_raw_json_records.py --record-id 216
```

This creates:

```text
authoring/kobotoolbox/records/raw/record_216_raw.json
authoring/kobotoolbox/records/raw/record_216_keys.txt
```

If no record ID is provided, the script uses the default record configured in the script.

## Step 2: Create or update the SSSOM file

After pulling the raw record, create or update the SSSOM mapping file.

The SSSOM file defines:

* source JSONPath from the Kobo raw JSON;
* target JSON-LD path;
* mapping predicate;
* confidence;
* transform rule;
* mapping comment.

The production SSSOM files are stored in:

```text
authoring/kobotoolbox/sssom/
```

For example:

```text
authoring/kobotoolbox/sssom/gaia_record217_tanzania_temp.sssom.tsv
```

Use the prompt templates in:

```text
authoring/kobotoolbox/prompts/
```

to support SSSOM creation and review. AI-generated mappings must be manually reviewed before use.

## Script 2: Transform SSSOM + raw JSON to JSON-LD

Use this script after the raw JSON and SSSOM TSV are ready.

Example for record 217:

```bash
python authoring/kobotoolbox/scripts/02_sssom_to_jsonld.py \
  --sssom authoring/kobotoolbox/sssom/gaia_record217_tanzania_temp.sssom.tsv \
  --input authoring/kobotoolbox/records/raw/record_217_raw.json \
  --output authoring/kobotoolbox/records/outputs/record_217_output.json \
  --wrap-key datasets
```

The `--wrap-key datasets` flag is important because the raw Kobo export is a single JSON object, while the SSSOM root path expects:

```text
$.datasets[*]
```

The flag temporarily wraps the raw record like this:

```json
{
  "datasets": [
    {
      "...": "raw Kobo record"
    }
  ]
}
```

No separate wrapped input file is created.

## Running another record

To process another record, change the record ID and filenames only.

Example for record 216:

```bash
python authoring/kobotoolbox/scripts/01_pull_kobo_raw_json_records.py --record-id 216
```

Then transform using the relevant SSSOM file:

```bash
python authoring/kobotoolbox/scripts/02_sssom_to_jsonld.py \
  --sssom authoring/kobotoolbox/sssom/<your_mapping_file>.sssom.tsv \
  --input authoring/kobotoolbox/records/raw/record_216_raw.json \
  --output authoring/kobotoolbox/records/outputs/record_216_output.json \
  --wrap-key datasets
```

## Important Notes

* Do not edit the scripts each time you change records.
* Use `--record-id` when pulling a new record.
* Use `--sssom`, `--input`, and `--output` when transforming a new record.
* Keep raw Kobo files in `records/raw/`.
* Keep generated JSON-LD files in `records/outputs/`.
* Keep mapping files in `sssom/`.
* Keep validation or comparison outputs in `records/validation/`.

## Recommended Environment

Use the Python 3.11 environment:

```bash
conda activate gdsc311
```

Then run commands from the repository root:

```bash
cd ~/Documents/Projects/ohdsi-gis-metadata-template
```

## Minimal Full Example

```bash
conda activate gdsc311

cd ~/Documents/Projects/ohdsi-gis-metadata-template

python authoring/kobotoolbox/scripts/01_pull_kobo_raw_json_records.py --record-id 217

python authoring/kobotoolbox/scripts/02_sssom_to_jsonld.py \
  --sssom authoring/kobotoolbox/sssom/gaia_record217_tanzania_temp.sssom.tsv \
  --input authoring/kobotoolbox/records/raw/record_217_raw.json \
  --output authoring/kobotoolbox/records/outputs/record_217_output.json \
  --wrap-key datasets
```
# KoboToolbox Scripts

This directory contains the scripts and notebooks used to transform metadata authored in KoboToolbox into machine-readable JSON-LD using JSONPath extraction and SSSOM mappings.

The workflow supports the Gaia Catalog metadata authoring process and provides a reproducible pipeline from raw Kobo records to Schema.org / Science-on-Schema.org compliant JSON-LD.

---

# Workflow Overview

```text
KoboToolbox Record
        │
        ▼
01_pull_kobo_raw_json_records.ipynb
        │
        ▼
record_<id>_raw.json
        │
        ▼
02_wrap_kobo_record.py
        │
        ▼
record_<id>_input.json
        │
        ▼
03_test_jsonpath_core_fields.py
03b_test_jsonpath_repeat_groups.py
        │
        ▼
04_create_kobo_sssom_crosswalk.py
        │
        ▼
gaia_metadata_authoring_form_v2_to_schemaorg.sssom.tsv
        │
        ▼
03_kobo_to_jsonld.py
        │
        ▼
record_<id>_output.jsonld
        │
        ▼
Validation & Comparison
```

---

# Script Descriptions

## 01_pull_kobo_raw_json_records.ipynb

Purpose:

Connects to the KoboToolbox API and retrieves metadata records from the Gaia Metadata Authoring Form.

Outputs:

* Raw Kobo JSON responses
* Individual record exports

Example output:

```text
records/raw/record_136_raw.json
```

---

## 02_wrap_kobo_record.py

Purpose:

Wraps a single Kobo record into the structure expected by the SSSOM transformation workflow.

Example:

Input:

```json
{
  "title": "Dataset Name"
}
```

Output:

```json
{
  "datasets": [
    {
      "title": "Dataset Name"
    }
  ]
}
```

This allows JSONPath expressions such as:

```text
$.datasets[*]
```

to work consistently.

---

## 03_test_jsonpath_core_fields.py

Purpose:

Tests JSONPath expressions against core metadata fields.

Examples:

```text
$.datasets[*]['dublin_core_group/title']
$.datasets[*]['dublin_core_group/description']
$.datasets[*]['dublin_core_group/doi']
```

Use this script whenever:

* A new form version is released
* Field names change
* A mapping fails

---

## 03b_test_jsonpath_repeat_groups.py

Purpose:

Tests JSONPath expressions for Kobo repeat groups.

Examples:

* Creators
* Publishers
* Coverage
* Subjects
* Dataset attributes

This script is useful for validating nested structures before building SSSOM mappings.

---

## 04_create_kobo_sssom_crosswalk.py

Purpose:

Creates or assists in generating an SSSOM crosswalk between Kobo field paths and Schema.org / Gaia Catalog target properties.

Outputs:

```text
sssom/gaia_metadata_authoring_form_v2_to_schemaorg.sssom.tsv
```

The crosswalk defines:

* Source JSONPath
* Target JSONPath
* Mapping justification
* Confidence
* Transformation rules

---

## 03_kobo_to_jsonld.py

Purpose:

Transforms Kobo JSON records into JSON-LD using:

* JSONPath extraction
* SSSOM mappings
* Transformation rules

This is the primary transformation script currently used by the Gaia Catalog workflow.

Inputs:

```text
records/raw/
sssom/
```

Outputs:

```text
records/outputs/
```

Example:

```text
record_136_raw.json
    ↓
record_136_output_v2.json
```

---

# Supporting Directories

## records/

Stores workflow artifacts:

```text
records/
├── raw/
├── outputs/
├── targets/
└── validation/
```

## sssom/

Stores mapping definitions:

```text
gaia_metadata_authoring_form_v2_to_schemaorg.sssom.tsv
```

## docs/

Contains workflow documentation and architecture notes.

---

# Validation Workflow

Generated JSON-LD should be compared against a target reference JSON-LD.

Example:

```text
record_136_output_v2.json
vs
record_136_target_pm25_vector_urban.json
```

Validation outputs are stored in:

```text
records/validation/
```

Examples:

```text
record_136_comparison_summary.md
record_136_diff_output_v2_vs_target.txt
```

---

# Notes

* The Gaia Metadata Authoring Form is the authoritative metadata source.
* JSONPath is used to extract values from Kobo records.
* SSSOM provides the mapping layer between Kobo metadata and Schema.org JSON-LD.
* Transformation rules may be required where source and target semantics differ.
* Generated JSON-LD should be validated and compared against reference examples before publication.

---

# Current Example Dataset

Record:

```text
136
```

Dataset:

```text
Annual PM2.5 Concentrations for Countries and Urban Areas, v1 (1998–2016)
```

This record is currently used as the primary reference implementation for developing and testing the Kobo → JSON-LD workflow.

