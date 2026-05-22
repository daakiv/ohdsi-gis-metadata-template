#!/usr/bin/env python3
"""
Transform a flat/wrapped JSON dataset file to JSON-LD using SSSOM mappings.

This version is adapted for the Kobo PM2.5 record 136 workflow.

Expected repository layout
--------------------------
authoring/
└── kobotoolbox/
    ├── scripts/
    │   └── sssom_to_jsonld.py
    └── mappings/
        └── SSSOM/
            └── kobo_record_136/
                ├── input/
                │   └── record_136_input.json
                ├── mappings/
                │   └── kobo_record_136.sssom.tsv
                └── output/
                    └── record_136_output.jsonld

Usage
-----
From authoring/kobotoolbox/scripts:

    python3 sssom_to_jsonld.py

Requires
--------
    python3 -m pip install pyyaml jsonpath-ng
"""

import csv
import io
import json
import re
from pathlib import Path
from typing import Any, Optional

import yaml
from jsonpath_ng.ext import parse as jp_parse


def parse_sssom(path: Path) -> tuple[dict, list[dict]]:
    """Return (metadata dict, list of mapping rows) from an SSSOM TSV file."""
    header_lines: list[str] = []
    data_lines: list[str] = []

    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.startswith("#"):
                if line.startswith("# "):
                    header_lines.append(line[2:])
                else:
                    header_lines.append(line[1:])
            else:
                data_lines.append(line)

    metadata = yaml.safe_load("".join(header_lines)) or {}
    reader = csv.DictReader(io.StringIO("".join(data_lines)), delimiter="\t")
    mappings = [
        row for row in reader
        if any((v or "").strip() for v in row.values())
    ]
    return metadata, mappings


def relative_path(full_path: str, root_path: str) -> str:
    """Convert an absolute source JSONPath to one relative to a matched root item."""
    root_base = re.sub(r"\[\*\]$", "", root_path.strip())
    suffix = full_path.strip()[len(root_base):]
    suffix = re.sub(r"^\[\*\]", "", suffix)
    return "$" + suffix


def leaf_name(target_jsonpath: str) -> Optional[str]:
    """Extract the property name from a simple '$.name' target JSONPath, else None.

    This follows Doug's initial simple transformation pattern. It handles targets
    like $.name, $.description, $.identifier, $.url, $.license, $.inLanguage.
    It skips nested targets such as $.distribution[0].contentUrl for now.
    """
    m = re.match(r"^\$\.(\w+)$", target_jsonpath.strip())
    return m.group(1) if m else None


def transform(input_data: dict, metadata: dict, mappings: list[dict]) -> dict:
    """Transform input JSON to JSON-LD using source_jsonpath and target_jsonpath."""
    curie_map = metadata.get("curie_map", {})

    class_row = next(
        (m for m in mappings if m.get("subject_category") == "owl:Class"),
        None,
    )

    if not class_row:
        raise ValueError(
            "No owl:Class mapping row found. "
            "Cannot determine source array path such as $.datasets[*]."
        )

    prop_rows = [
        m for m in mappings
        if m.get("subject_category") == "owl:ObjectProperty"
    ]

    root_src_path = class_row["source_jsonpath"].strip()
    target_type = class_row["object_id"].strip()

    source_items = [m.value for m in jp_parse(root_src_path).find(input_data)]

    records: list[dict[str, Any]] = []

    for item in source_items:
        record: dict[str, Any] = {"@type": target_type}

        for row in prop_rows:
            src = row.get("source_jsonpath", "").strip()
            tgt = row.get("target_jsonpath", "").strip()

            if not src or not tgt:
                continue

            rel = relative_path(src, root_src_path)

            try:
                matches = jp_parse(rel).find(item)
            except Exception as err:
                print(f"Skipping invalid source_jsonpath: {src}")
                print(f"  Error: {err}")
                continue

            if not matches:
                continue

            values = [m.value for m in matches]
            prop = leaf_name(tgt)

            if prop:
                record[prop] = values if len(values) > 1 else values[0]
            else:
                print(f"Skipping complex target_jsonpath for now: {tgt}")

        records.append(record)

    schema_base = curie_map.get("schema", "https://schema.org/")

    context = {
        "@vocab": schema_base,
        "schema": schema_base,
    }

    for prefix in ["dct", "dcat", "gdsc"]:
        if prefix in curie_map:
            context[prefix] = curie_map[prefix]

    return {
        "@context": context,
        "@graph": records,
    }


def main() -> None:
    script_dir = Path(__file__).resolve().parent

    # script_dir = authoring/kobotoolbox/scripts
    # kobo_dir   = authoring/kobotoolbox
    kobo_dir = script_dir.parent

    sssom_path = (
        kobo_dir
        / "mappings"
        / "SSSOM"
        / "kobo_record_136"
        / "mappings"
        / "kobo_record_136.sssom.tsv"
    )

    input_path = (
        kobo_dir
        / "mappings"
        / "SSSOM"
        / "kobo_record_136"
        / "input"
        / "record_136_input.json"
    )

    output_path = (
        kobo_dir
        / "mappings"
        / "SSSOM"
        / "kobo_record_136"
        / "output"
        / "record_136_output.jsonld"
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)

    print("SSSOM file:")
    print(sssom_path)

    print("\nInput file:")
    print(input_path)

    print("\nOutput file:")
    print(output_path)

    if not sssom_path.exists():
        raise FileNotFoundError(f"Could not find SSSOM file: {sssom_path}")

    if not input_path.exists():
        raise FileNotFoundError(f"Could not find input JSON file: {input_path}")

    print(f"\nParsing {sssom_path.name} ...")
    metadata, mappings = parse_sssom(sssom_path)
    print(f"  {len(mappings)} mapping row(s) loaded")

    with open(input_path, encoding="utf-8") as fh:
        input_data = json.load(fh)

    print(f"\nTransforming {input_path.name} ...")
    jsonld = transform(input_data, metadata, mappings)
    print(f"  {len(jsonld['@graph'])} dataset record(s) mapped")

    with open(output_path, "w", encoding="utf-8") as fh:
        json.dump(jsonld, fh, indent=2, ensure_ascii=False)

    print("\nOutput written to:")
    print(output_path)


if __name__ == "__main__":
    main()