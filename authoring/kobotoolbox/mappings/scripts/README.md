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

Use the AI mapping prompt template:

[Transform Prompt Template](../prompts/transform_prompt_template.md)

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


```

## Important Notes

* Do not edit the scripts each time you change records.
* Use `--record-id` when pulling a new record.
* Use `--sssom`, `--input`, and `--output` when transforming a new record.
* Keep raw Kobo files in `records/raw/`.
* Keep generated JSON-LD files in `records/outputs/`.
* Keep mapping files in `sssom/`.
* Keep validation or comparison outputs in `records/validation/`.


