# Prompts

This folder stores AI prompt templates used to support the KoboToolbox → JSONPath → SSSOM → JSON-LD workflow.

The prompts are intended to help with structured metadata mapping tasks while reducing hallucination risk. They should be used as drafting and review aids, not as final authority.

## Purpose

These prompts support:

- identifying fields in raw KoboToolbox JSON records;
- testing and explaining JSONPath expressions;
- generating or reviewing SSSOM mapping rows;
- comparing generated JSON-LD outputs against target reference files;
- documenting unmapped fields, transformation decisions, and validation notes.

## Main Prompt Types

### SSSOM mapping prompts

Used to generate or review SSSOM TSV mappings between KoboToolbox fields and Schema.org / Science-on-Schema.org JSON-LD properties.

These prompts should always include:

- the raw Kobo JSON record;
- the existing SSSOM TSV, if extending a mapping;
- strict source JSONPath rules;
- allowed target properties;
- known transform rules;
- hallucination guard instructions.

### Validation prompts

Used to compare generated JSON-LD output against a target JSON-LD reference file and identify missing, extra, or structurally different properties.

### Hallucination guard prompts

Used to check whether proposed mappings are grounded in the actual raw JSON, use valid Schema.org/DCT/DCAT properties, and avoid invented JSONPaths or transform rules.

## Current Reference Example

The current reference workflow uses record 136:

```text
records/raw/record_136_raw.json

