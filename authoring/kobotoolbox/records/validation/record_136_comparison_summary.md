# Record 136 JSON-LD Comparison Summary

This comparison reviews the generated JSON-LD output from the Kobo → SSSOM transformation against the target PM2.5 vector urban JSON-LD profile.

## Files compared

- Generated output: `records/outputs/record_136_output_v2_local.json`
- Target reference: `records/targets/record_136_target_pm25_vector_urban.json`
- Diff output: `records/validation/record_136_diff_output_v2_vs_target.txt`

## Overall status

The transformation is working. The generated output captures the core Schema.org Dataset structure and several enriched fields, including:

- `@id`
- `identifier`
- `name`
- `description`
- `license`
- `creator`
- `provider`
- `spatialCoverage`
- `includedInDataCatalog`
- `measurementTechnique`
- `distribution`
- `variableMeasured`
- `isAccessibleForFree`

## Main remaining gaps

The target contains additional enriched properties that are not fully produced from the current Kobo record and SSSOM transformation:

- `version`
- `hasPart`
- `about`
- `isBasedOn`
- `subjectOf`
- richer `spatialCoverage.geo.box`
- Gaia download distributions
- full 1998–2016 PM2.5 variables
- `minValue` and `maxValue` for annual PM2.5 variables
- richer workflow and provenance metadata

## Interpretation

Most remaining gaps are not simple one-to-one Kobo field mappings. They require either Gaia defaults, ETL-derived values, GIS-derived values, workflow documentation, or manual curation.

## Next action

Review which missing target fields should be:

1. added to the Kobo form,
2. derived during transformation,
3. generated from Gaia defaults,
4. computed during ETL/GIS processing, or
5. manually curated.
